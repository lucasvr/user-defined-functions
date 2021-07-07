def dynamic_dataset():
    from telnetlib import Telnet

    with Telnet('127.0.0.1', 23) as telnet:
        # Read one frame from the telnet server
        telnet.read_until(b"!start!\r\n")
        data = telnet.read_until(b"!end!\r\n").decode('ascii')
        frame = data[0:data.find("\r\n!end!")]
        
        # Write the frame to the HDF5 dataset
        output = lib.getData("star_wars")
        for i, row in enumerate(frame.split('\r\n')):
            lib.setString(output[i], row.encode('utf-8'))
