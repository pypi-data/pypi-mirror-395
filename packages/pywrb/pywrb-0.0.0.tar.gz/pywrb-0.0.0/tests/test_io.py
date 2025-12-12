import pathlib

import numpy

from pywrb import WRB_BLOCK_MEANING, WRB_UNIT, WRBFile


def test_io(tmp_path):
    data = numpy.linspace(0, 1, 10)[:, numpy.newaxis] * numpy.linspace(0, 1, 10)
    with WRBFile(
        filename=tmp_path / "test.wrb",
        mode="wb",
        crs="EPSG:25832",
        minx=0,
        miny=0,
        maxx=900,
        maxy=900,
        resolutionx=100,
        resolutiony=100,
        heights=[10],
        wind_speeds=[],
        directions=0,
    ) as wrb:
        wrb.add_block(data=data, meaning=WRB_BLOCK_MEANING.ELEVATION, unit=WRB_UNIT.METER)
        wrb.add_block(
            data=data + 1, meaning=WRB_BLOCK_MEANING.MEAN_WIND_SPEED, height=10, unit=WRB_UNIT.METER_PER_SECOND
        )
        wrb.write()

    with WRBFile(filename=tmp_path / "test.wrb") as wrb:
        assert (len(wrb.blocks)) == 2

        assert wrb.blocks[0]["meaning"] == WRB_BLOCK_MEANING.ELEVATION
        assert wrb.blocks[0]["unit"] == WRB_UNIT.METER

        numpy.testing.assert_allclose(wrb.read_block(0), data)

        assert wrb.blocks[1]["meaning"] == WRB_BLOCK_MEANING.MEAN_WIND_SPEED
        assert wrb.blocks[1]["unit"] == WRB_UNIT.METER_PER_SECOND
        numpy.testing.assert_allclose(wrb.read_block(1), data + 1)


def test_write_real(tmp_path):
    data = numpy.linspace(0, 1, 10)[:, numpy.newaxis] * numpy.linspace(0, 1, 10)

    probability = numpy.random.rand(16, 10, 10) * 100
    number_of_directions = 30
    directions = numpy.linspace(0, 360, number_of_directions, endpoint=False)
    heights = range(0, 100, 10)

    with WRBFile(
        filename=tmp_path / "test.wrb",
        mode="wb",
        crs="EPSG:25832",
        minx=0,
        miny=0,
        maxx=900,
        maxy=900,
        resolutionx=100,
        resolutiony=100,
        directions=number_of_directions,
        heights=heights,
        wind_speeds=[],
    ) as wrb:
        wrb.add_block(data=data, meaning=WRB_BLOCK_MEANING.ELEVATION, unit=WRB_UNIT.METER)
        wrb.add_block(
            data=data + 1, meaning=WRB_BLOCK_MEANING.MEAN_WIND_SPEED, height=100, unit=WRB_UNIT.METER_PER_SECOND
        )
        for direction in directions:
            for height in heights:
                for i in range(probability.shape[0]):
                    wrb.add_block(
                        data=probability[i],
                        meaning=WRB_BLOCK_MEANING.PROBABILITY,
                        height=height,
                        direction=float(direction),
                        unit=WRB_UNIT.PERCENT,
                    )
                    wrb.add_block(
                        data=data,
                        meaning=WRB_BLOCK_MEANING.WEIBULL_SCALE,
                        height=height,
                        direction=float(direction),
                        unit=WRB_UNIT.METER_PER_SECOND,
                    )
                    wrb.add_block(
                        data=data, meaning=WRB_BLOCK_MEANING.WEIBULL_SHAPE, height=height, direction=float(direction)
                    )

        wrb.write()


def test_read_real_world(tmp_path):
    with WRBFile(pathlib.Path(__file__).parent / "fixtures/real_world.wrb") as wrb:
        assert len(wrb.blocks) == 69
        assert wrb.shape == (127, 127)
        assert wrb.minx == 439887.0
        assert wrb.maxx == 465087.0
        assert wrb.miny == 4833898.0
        assert wrb.maxy == 4859098.0
        assert wrb.resolutionx == 200
        assert wrb.resolutiony == 200
        assert wrb.number_of_wind_directions == 16
        assert wrb.number_of_heights == 1
        assert wrb.number_of_wind_speeds == 0

        numpy.testing.assert_allclose(wrb.heights, numpy.array([80.0]))
        numpy.testing.assert_allclose(
            wrb.directions, numpy.linspace(0, 360, wrb.number_of_wind_directions, endpoint=False)
        )
        numpy.testing.assert_allclose(wrb.wind_speeds, numpy.array([]))

        with WRBFile(
            tmp_path / "test.wrb",
            mode="wb",
            crs=wrb.crs,
            minx=wrb.minx,
            miny=wrb.miny,
            maxx=wrb.maxx,
            maxy=wrb.maxy,
            resolutionx=wrb.resolutionx,
            resolutiony=wrb.resolutiony,
            directions=wrb.number_of_wind_directions,
            heights=wrb.heights,
            wind_speeds=wrb.wind_speeds,
        ) as write_wrb:
            for block, data in wrb:
                write_wrb.add_block(data=data, **block)
            write_wrb.write()

    # with WRBReader(filename=tmp_path /"test.wrb") as wrb:
    #     wrb.read()
