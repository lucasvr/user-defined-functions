# Virtualization of CSV files through HDF5-UDF

def dynamic_dataset():
    udf_data = lib.getData("GreatestAlbums")
    udf_dims = lib.getDims("GreatestAlbums")

    # The file is encoded as ISO-8859-1, so instruct Python about it
    with open("albumlist.csv", encoding="iso-8859-1") as f:

        # Read and ignore the header
        f.readline()

        for i, line in enumerate(f.readlines()):
            # Remove double-quotes and newlines around certain strings
            parts = [col.strip('"').strip("\n") for col in line.split(",")]

            # Note: unless we specify 'string(N)' with a large enough N, we
            # may end up attempting to write more characters into the string
            # buffer than allowed. Here we use the lib.setString() API so it
            # performs boundary checks for us. The alternative is to write
            # directly to each udf_data[i] member, at the risk of receiving
            # a FFI exception if more data is attempted to be copied than
            # allowed. Again, note that, when '(N)' is absent, the default
            # string member size is of 32 characters.
            udf_data[i].Number = int(parts[0])
            udf_data[i].Year = int(parts[1])
            lib.setString(udf_data[i].Album,  parts[2].encode("utf-8"))
            lib.setString(udf_data[i].Artist,  parts[3].encode("utf-8"))
            lib.setString(udf_data[i].Genre,  parts[4].encode("utf-8"))
            lib.setString(udf_data[i].Subgenre,  parts[5].encode("utf-8"))
