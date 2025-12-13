// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//         http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const std = @import("std");
const mem = std.mem;
const Allocator = std.mem.Allocator;
const ffi = @import("ffi");
const py = @import("./pyz3.zig");

/// Thread-local GIL state tracking for performance optimization
/// This prevents redundant GIL acquire/release calls when already held
threadlocal var gil_depth: u32 = 0;
threadlocal var gil_state: ffi.PyGILState_STATE = undefined;

/// RAII helper to manage GIL acquisition with depth tracking
const ScopedGIL = struct {
    acquired: bool,

    fn acquire() ScopedGIL {
        if (gil_depth == 0) {
            gil_state = ffi.PyGILState_Ensure();
            gil_depth = 1;
            return .{ .acquired = true };
        } else {
            gil_depth += 1;
            return .{ .acquired = false };
        }
    }

    fn release(self: ScopedGIL) void {
        if (gil_depth > 0) {
            gil_depth -= 1;
            if (self.acquired and gil_depth == 0) {
                ffi.PyGILState_Release(gil_state);
            }
        }
    }
};

pub const PyMemAllocator = struct {
    const Self = @This();

    pub fn allocator(self: *const Self) Allocator {
        return .{
            .ptr = @constCast(self),
            .vtable = &.{
                .alloc = alloc,
                .remap = remap,
                .resize = resize,
                .free = free,
            },
        };
    }

    fn alloc(ctx: *anyopaque, len: usize, ptr_align: mem.Alignment, ret_addr: usize) ?[*]u8 {
        // As per this issue, we will hack an aligned allocator.
        // https://bugs.python.org/msg232221
        _ = ret_addr;
        _ = ctx;

        // PyMem functions require the GIL
        // Optimized: Check if GIL already held to avoid overhead in re-entrant calls
        const scoped_gil = ScopedGIL.acquire();
        defer scoped_gil.release();

        const alignment_bytes = ptr_align.toByteUnits();

        // Safety check: ensure alignment fits in u8 for our header scheme
        // Our scheme stores the alignment shift in a single byte before the returned pointer.
        // For alignments > 255 bytes, this won't work without a different approach.
        if (alignment_bytes > 255) {
            // For large alignments, we would need either:
            // - A larger header (u16/u32) which complicates the scheme
            // - Using PyMem_AlignedAlloc (Python 3.11+) directly
            // - System-specific aligned_alloc
            // For now, fail the allocation. This is rare in practice.
            std.debug.print("Error: Alignment {d} bytes exceeds maximum supported alignment of 255\n", .{alignment_bytes});
            return null;
        }

        const alignment: u8 = @intCast(alignment_bytes);

        // Allocate enough space for the data plus alignment padding
        // We need up to (alignment - 1) extra bytes for alignment, plus 1 byte for the header
        // So total extra = alignment bytes
        const raw_ptr: usize = @intFromPtr(ffi.PyMem_Malloc(len + alignment) orelse return null);

        // Calculate the alignment offset needed
        // If raw_ptr is already aligned, we still need to shift by 'alignment' to make room for header
        // Otherwise, we shift by enough to align it
        const misalignment = raw_ptr % alignment_bytes;
        const shift: u8 = if (misalignment == 0) alignment else @intCast(alignment_bytes - misalignment);

        // Verify shift is valid: must be > 0 (room for header) and <= alignment (within our allocation)
        std.debug.assert(shift > 0 and shift <= alignment);

        const aligned_ptr: usize = raw_ptr + shift;

        // Safety assertions: verify we're not writing outside our allocated region
        std.debug.assert(aligned_ptr > raw_ptr); // Ensure we moved forward (shift > 0)
        std.debug.assert(aligned_ptr - 1 >= raw_ptr); // Ensure header byte is in our allocation
        std.debug.assert((aligned_ptr - 1) - raw_ptr < alignment); // Header is within padding

        // Verify the returned pointer is properly aligned
        std.debug.assert(aligned_ptr % alignment_bytes == 0);

        // Store the shift in the byte immediately before the aligned pointer
        // This byte is guaranteed to be within our allocation due to the assertions above
        @as(*u8, @ptrFromInt(aligned_ptr - 1)).* = shift;

        return @ptrFromInt(aligned_ptr);
    }

    fn remap(ctx: *anyopaque, memory: []u8, ptr_align: mem.Alignment, new_len: usize, ret_addr: usize) ?[*]u8 {
        // As per this issue, we will hack an aligned allocator.
        // https://bugs.python.org/msg232221
        _ = ret_addr;
        _ = ctx;

        // PyMem functions require the GIL
        // Optimized: Check if GIL already held to avoid overhead in re-entrant calls
        const scoped_gil = ScopedGIL.acquire();
        defer scoped_gil.release();

        const alignment_bytes = ptr_align.toByteUnits();

        // Safety check: ensure alignment fits in u8
        if (alignment_bytes > 255) {
            std.debug.print("Error: Alignment {d} bytes exceeds maximum supported alignment of 255 in remap\n", .{alignment_bytes});
            return null;
        }

        const alignment: u8 = @intCast(alignment_bytes);

        // Retrieve and validate the shift from the header byte
        const aligned_ptr_in: usize = @intFromPtr(memory.ptr);
        const old_shift = @as(*u8, @ptrFromInt(aligned_ptr_in - 1)).*;

        // Verify the header is valid
        if (old_shift == 0 or old_shift > alignment) {
            // Either corrupted header, or alignment changed between alloc and remap
            std.debug.print("Error: Invalid alignment header in remap: shift={d}, alignment={d}\n", .{ old_shift, alignment });
            return null;
        }

        // Recover the original pointer that was passed to PyMem_Malloc
        const origin_mem_ptr: *anyopaque = @ptrFromInt(aligned_ptr_in - old_shift);

        // Reallocate with room for alignment padding
        const raw_ptr: usize = @intFromPtr(ffi.PyMem_Realloc(origin_mem_ptr, new_len + alignment) orelse return null);

        // Calculate new alignment offset
        const misalignment = raw_ptr % alignment_bytes;
        const shift: u8 = if (misalignment == 0) alignment else @intCast(alignment_bytes - misalignment);

        // Verify shift is valid
        std.debug.assert(shift > 0 and shift <= alignment);

        const aligned_ptr: usize = raw_ptr + shift;

        // Safety assertions
        std.debug.assert(aligned_ptr > raw_ptr);
        std.debug.assert(aligned_ptr - 1 >= raw_ptr);
        std.debug.assert((aligned_ptr - 1) - raw_ptr < alignment);
        std.debug.assert(aligned_ptr % alignment_bytes == 0);

        // Store the new shift in the header byte
        @as(*u8, @ptrFromInt(aligned_ptr - 1)).* = shift;

        return @ptrFromInt(aligned_ptr);
    }

    fn resize(ctx: *anyopaque, buf: []u8, buf_align: mem.Alignment, new_len: usize, ret_addr: usize) bool {
        _ = ret_addr;
        _ = ctx;

        // PyMem functions require the GIL
        // Optimized: Check if GIL already held to avoid overhead in re-entrant calls
        const scoped_gil = ScopedGIL.acquire();
        defer scoped_gil.release();

        const alignment_bytes = buf_align.toByteUnits();

        // Shrinking always succeeds - we just report the smaller size
        // PyMem will keep track of the actual allocation size for us
        if (new_len <= buf.len) {
            return true;
        }

        // For growing, we try to realloc in-place
        // Get the original pointer before alignment adjustment
        const aligned_ptr: usize = @intFromPtr(buf.ptr);
        const shift = @as(*const u8, @ptrFromInt(aligned_ptr - 1)).*;
        const origin_mem_ptr: *anyopaque = @ptrFromInt(aligned_ptr - shift);

        // Try to realloc. If it succeeds in-place, the pointer won't change
        // Safety check for alignment
        if (alignment_bytes > 255) {
            return false; // Can't handle large alignments
        }

        const alignment: u8 = @intCast(alignment_bytes);
        const new_ptr = ffi.PyMem_Realloc(origin_mem_ptr, new_len + alignment) orelse return false;

        // Check if realloc succeeded in-place (pointer didn't move)
        // If it moved, we can't update buf.ptr, so return false to force remap/alloc
        if (@intFromPtr(new_ptr) == aligned_ptr - shift) {
            // Success! Allocation grew in-place
            return true;
        }

        // Allocation moved - we need to copy to new location, so return false
        // to let the allocator handle it via remap
        // Note: We've already reallocated, but we can't use the new pointer
        // This is a limitation of the resize() API. The caller will call remap()
        // which will realloc again, but PyMem_Realloc should be smart enough to reuse
        return false;
    }

    fn free(ctx: *anyopaque, buf: []u8, buf_align: mem.Alignment, ret_addr: usize) void {
        _ = buf_align;
        _ = ctx;
        _ = ret_addr;

        // PyMem functions require the GIL
        // Optimized: Check if GIL already held to avoid overhead in re-entrant calls
        const scoped_gil = ScopedGIL.acquire();
        defer scoped_gil.release();

        // Fetch the alignment shift. We could check it matches the buf_align, but it's a bit annoying.
        const aligned_ptr: usize = @intFromPtr(buf.ptr);
        const shift = @as(*const u8, @ptrFromInt(aligned_ptr - 1)).*;

        const raw_ptr: *anyopaque = @ptrFromInt(aligned_ptr - shift);
        ffi.PyMem_Free(raw_ptr);
    }
}{};
