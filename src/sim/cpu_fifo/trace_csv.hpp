#pragma once

#include <cstddef>
#include <string>
#include <vector>

#include "types.hpp"

namespace sim::cpu_fifo::trace_csv
{

    struct TraceReadOptions
    {
        bool enforce_header = true;
        bool enforce_sorted_timestamps = true;
        char delimiter = ',';
    };

    struct TraceReadResult
    {
        std::vector<Packet> packets;
        std::size_t row_count = 0;
        std::size_t skipped_rows = 0;
    };

    TraceReadResult read_trace_csv(
        const std::string &path,
        const TraceReadOptions &options = {});

} // namespace sim::cpu_fifo::trace_csv
