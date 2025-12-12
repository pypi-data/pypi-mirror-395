# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

# this package
from kraken_decompressor import decompress

data_dir = PathPlus(__file__).parent.abspath()


@pytest.mark.parametrize(
		"compressed_file, reference_file",
		[
				("image.bin", "Hendrik_Voogd_-_Italian_landscape_with_Umbrella_Pines.jpg"),
				("text.bin", "example_text.txt"),
				]
		)
def test_decompression(compressed_file: str, reference_file: str):
	compressed_data = data_dir.joinpath(compressed_file).read_bytes()
	reference_data = data_dir.joinpath(reference_file).read_bytes()

	assert compressed_data[:4] == b"KARK"
	size = int.from_bytes(compressed_data[4:8], "little")
	assert size == len(reference_data)
	assert decompress(compressed_data[8:], size) == reference_data
