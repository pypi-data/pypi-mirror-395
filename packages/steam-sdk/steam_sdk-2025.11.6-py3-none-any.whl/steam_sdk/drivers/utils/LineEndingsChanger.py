for file_name in ['call_mainfiqus_htcondor.sh', 'call_ledet_htcondor.sh']:
    with open(file_name, "rb") as f:
        data = f.read()

    # replace CRLF (0x0D 0x0A) with LF (0x0A)
    data = data.replace(b"\r\n", b"\n")

    with open(file_name, "wb") as f:
        f.write(data)
