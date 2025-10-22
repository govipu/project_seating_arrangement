#!/usr/bin/env python3
"""Entry point for the seating arrangement tool."""

import argparse
import sys
from seating_allocator import SeatingAllocator
from logger_setup import setup_logging


def parse_args():
    p = argparse.ArgumentParser(description="Generate seating arrangement for exams.")
    p.add_argument('--input', '-i', required=True, help='Input Excel file (timetable + lists)')
    p.add_argument('--buffer', '-b', type=int, default=0, help='Buffer seats (e.g. 5 means reduce each room capacity by 5)')
    p.add_argument('--density', '-d', choices=['Sparse', 'Dense'], default='Dense', help='Sparse or Dense seating')
    p.add_argument('--outdir', '-o', default='output', help='Output folder (will be created)')
    return p.parse_args()


def main():
    args = parse_args()
    logger = setup_logging('seating.log', 'errors.txt')
    logger.info('Starting seating arrangement')

    try:
        alloc = SeatingAllocator(
            input_file=args.input,
            buffer=args.buffer,
            density=args.density,
            outdir=args.outdir,
            logger=logger
        )

        # Step 1: Load input sheets
        alloc.load_inputs()

        # Step 2: Perform all allocations
        alloc.allocate_all_days()

        # Step 3: Write the output Excel files
        alloc.write_outputs()

        logger.info('✅ Completed seating allocation successfully!')

    except Exception as e:
        logger.exception('Fatal error in main: %s', e)
        print('⚠️ An error occurred. Check errors.txt and seating.log for details.')
        sys.exit(1)


if __name__ == '__main__':
    main()
