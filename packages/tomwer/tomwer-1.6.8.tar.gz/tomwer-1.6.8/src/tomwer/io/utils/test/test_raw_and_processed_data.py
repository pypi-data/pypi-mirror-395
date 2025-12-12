from tomwer.io.utils.raw_and_processed_data import file_is_on_processed_data


def test_file_is_on_processed_data():
    """test file_is_on_processed_data function"""
    assert file_is_on_processed_data("/path/to/file") == False
    assert file_is_on_processed_data("/path/to/PROCESSED_DATA/file") == True
    assert file_is_on_processed_data("/path/to/RAW_DATA/file") == False
    assert file_is_on_processed_data("/path/to/RAW_DATA/PROCESSED_DATA/file") == True
    assert file_is_on_processed_data("/path/to/PROCESSED_DATA/RAW_DATA/file") == False
