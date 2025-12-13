# from MDUS.Class import DatasClass

#セッティングは各自に
def datasload(self,start=None,end=None,orbit=None):
    datatype = self.info["Input Data"]
    tmp = []
    for d in datatype:
        self.value[d].Load(start=start,end=end,orbit=orbit)
        if self.value[d] is not None:
            tmp.append(d)
    self.info["Load Success"] = tmp

# DatasClass.Datas.Load = datasload