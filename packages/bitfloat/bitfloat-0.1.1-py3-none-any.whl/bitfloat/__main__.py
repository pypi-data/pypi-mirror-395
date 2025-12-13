"""Command-line interface for bitfloat."""

import sys
from bitfloat import F32, F64, F16, BF16, F8E4M3, F8E5M2, F4E2M1, BF24


# Format name to class mapping
FORMAT_MAP = {
    "f32": F32,
    "f64": F64,
    "f16": F16,
    "bf16": BF16,
    "bf24": BF24,
    "f8e4m3": F8E4M3,
    "f8e5m2": F8E5M2,
    "f4e2m1": F4E2M1,
}


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: bitfloat <value> [format]")
        print("  value: float number or hex (0x...)")
        print("  format: f32 (default), f64, f16, bf16, bf24, f8e4m3, f8e5m2, f4e2m1")
        print()
        print("Examples:")
        print("  bitfloat 3.14")
        print("  bitfloat 3.14 f16")
        print("  bitfloat 0x3f800000")
        print("  bitfloat 0x00000001 f16")
        sys.exit(1)

    value_str = sys.argv[1]
    format_name = sys.argv[2].lower() if len(sys.argv) > 2 else "f32"

    # Get the format class
    format_class = FORMAT_MAP.get(format_name, F32)

    # Parse the value
    if value_str.startswith("0x") or value_str.startswith("0X"):
        # Hex input - treat as bit pattern
        int_value = int(value_str, 16)
        bf = format_class.from_int(int_value)
    else:
        # Float input
        float_value = float(value_str)
        bf = format_class.from_float(float_value)

    # Print the result
    print(bf)


if __name__ == "__main__":
    main()
