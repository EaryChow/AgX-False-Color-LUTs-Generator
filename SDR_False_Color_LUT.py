import colour
import numpy

# define breaking points, numbers are percentages
white_lower = 93
red_lower = 80
orange_lower = 55
yellow_lower = 35
green_yellow_lower = 22
mid_grey_lower = 16
green_cyan_lower = 5
cyan_lower = 0.5
blue_cyan_lower = 0.02
blue_lower = 0.005
black_lower = 0.0005


def main():
    # resolution of the 3DLUT
    LUT_res = 45

    LUT = colour.LUT3D(name=f'False Color LUT for AgX Imagery',
                       size=LUT_res)

    LUT.domain = ([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
    LUT.comments = [f'A Post Formation False Color LUT for AgX Image Formation',
                    f'This LUT expects values from 0.0 to 1.0, with inverse power function of 3.0 for precision reason']

    x, y, z, _ = LUT.table.shape

    for i in range(x):
        for j in range(y):
            for k in range(z):
                col = numpy.array(LUT.table[i][j][k], dtype=numpy.longdouble)

                col = colour.models.exponent_function_basic(col, 3.0, 'basicFwd')

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

                LUT.table[i][j][k] = numpy.array(col, dtype=LUT.table.dtype)

    colour.write_LUT(
        LUT,
        f"AgX_False_Color.cube")
    print(LUT)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
