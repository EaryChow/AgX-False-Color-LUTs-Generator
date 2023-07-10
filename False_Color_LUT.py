import colour
import numpy
import pathlib

output_config_directory = ""
output_LUTs_directory = ""
x_input = numpy.linspace([0.00, 0.00, 0.00], [1.00, 1.00, 1.00], 4096)

# define breaking points, numbers are percentages
white_lower = 97
red_lower = 80
orange_lower = 55
yellow_lower = 35
green_yellow_lower = 22
mid_grey_lower = 16
green_cyan_lower = 5
cyan_lower = 0.5
blue_cyan_lower = 0.05
blue_lower = 0.0001
black_lower = 0


def false_color(col):
    # col = colour.models.exponent_function_basic(col, 3.0, 'basicFwd')

    col = col * 100

    original = col

    # black zone
    col = colour.algebra.lerp(numpy.greater(original, black_lower), col, [0.0, 0.0, 0.0])

    # blue zone
    col = colour.algebra.lerp(numpy.greater(original, blue_lower), col, [0.0, 0.0, 1.0])

    # blue cyan zone
    col = colour.algebra.lerp(numpy.greater(original, blue_cyan_lower), col, [0.0, 0.5, 1.0])

    # cyan zone
    col = colour.algebra.lerp(numpy.greater(original, cyan_lower), col, [0.0, 1.0, 1.0])

    # green cyan zone
    col = colour.algebra.lerp(numpy.greater(original, green_cyan_lower), col, [0.0, 1.0, 0.5])

    # middle grey zone
    col = colour.algebra.lerp(numpy.greater(original, mid_grey_lower), col, [0.5, 0.5, 0.5])

    # green yellow zone
    col = colour.algebra.lerp(numpy.greater(original, green_yellow_lower), col, [0.5, 1, 0.0])

    # yellow zone
    col = colour.algebra.lerp(numpy.greater(original, yellow_lower), col, [1.0, 1.0, 0.0])

    # orange zone
    col = colour.algebra.lerp(numpy.greater(original, orange_lower), col, [1.0, 0.5, 0.0])

    # red zone
    col = colour.algebra.lerp(numpy.greater(original, red_lower), col, [1.0, 0.0, 0.0])

    # white zone
    col = colour.algebra.lerp(numpy.greater(original, white_lower), col, [1.0, 1.0, 1.0])

    return col


y_LUT = false_color(x_input)

LUT_name = "AgX_False_Color"
LUT_safe = LUT_name.replace(" ", "_")
LUT = colour.LUT3x1D(
    table=y_LUT,
    name="AgX_False_Color"
)

try:
    output_directory = pathlib.Path(output_config_directory)
    LUTs_directory = output_directory / output_LUTs_directory
    LUT_filename = pathlib.Path(
        LUTs_directory / "{}.spi1d".format(LUT_safe)
    )
    LUTs_directory.mkdir(parents=True, exist_ok=True)
    colour.io.luts.write_LUT(LUT, LUT_filename, method="Sony SPI1D")
    print(LUT)
except Exception as ex:
    raise ex

