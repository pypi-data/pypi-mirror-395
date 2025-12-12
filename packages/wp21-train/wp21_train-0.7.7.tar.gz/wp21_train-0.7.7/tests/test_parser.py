import sys
import os

import wp21_train as train

def main():
    parser = train.parser.hls_parser("/home/ixiotidi/Development/hw-aware-training/tf_model/model_0/hls4ml_prj/myproject_prj/solution1/syn/report/csynth.xml")

    print(parser._data)
    print(parser._meta_data)


if __name__=="__main__":
    main()
