import Mcrawl as mcr
import Mwordcloud as mwc

if __name__=="__main__":
    print("프로그램 시작~~")
    mcrawl = mcr.Mcrawl()
    mcrawl.excute(keyword="제임스웹",start_dt='2022.07.15',from_dt='2022.07.23',limit=100)

    mwordcloud = mwc.Mwc()
    mwordcloud.execute()

    print("프로그램 종료....")
    
