def read_and_write(filename, data) -> bool:
    with open(file=filename, mode='a+', encoding='utf-8') as f:
        f.seek(0)
        datas = f.read()
        if data not in datas:
            f.write(data + '\n')
            return True
        return False
