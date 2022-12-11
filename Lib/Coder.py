
class Coder:
    def encode(self):
        pass

    def decode(self, rawData):
        pass


class FGOCoder(Coder):
    def encode(self):
        pass

    def decode(self, rawData):
        # DO:
        # 输入：方案的值
        # 输出： {“参数名”：['参数值1','参数值2']}
        result = [data for data in rawData.split(",")]

        # for data in rawData:
        #     result[data.split(":")[0]] = data.split(":")[1].split(",")
        print(result)
        return result


class PCRShopCoder(Coder):
    def decode(self, **kwargs):
        # DO:
        # 将输入的所有参数，编入一个字典，并返回
        result = {}
        print(kwargs)

        for k in kwargs:
            result[k] = []
            kwargs[k] = str(kwargs[k])
            for data in kwargs[k].split(","):
                if data != "":
                    result[k].append(int(data))

        return result


class ListCoder(Coder):
    def decode(self, rawData):
        # DO:
        # 输入："字,符"
        # 输出：["字","符"]
        result = []
        for word in rawData.split(","):
            result.append(word)

        return result


if __name__ == "__main__":
    print(PCRShopCoder().decode(s1="1,2,3",s2=""))
