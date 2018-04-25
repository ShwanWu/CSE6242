// Guangxu Chen
#include <iostream>
#include <cstdlib>
#include <fstream>
#include <cstring>
#include <vector>


#include <direct.h>
#include <io.h>


using namespace std;
#include "Image.h"

vector<string> getFiles(string path)
{
    vector<string> files;//存放文件名


    //文件句柄
    long   hFile   =   0;
    //文件信息
    struct _finddata_t fileinfo;
    string p;
    if((hFile = _findfirst(p.assign(path).append("\\*").c_str(),&fileinfo)) !=  -1)
    {
        do
        {
            if(fileinfo.name[0] != '.')
                files.push_back(string(fileinfo.name) );
        }while(_findnext(hFile, &fileinfo)  == 0);
        _findclose(hFile);
    }



    //排序，按从小到大排序
    sort(files.begin(), files.end());
    return files;
}

int main(int argc, char** argv)
{
    if (argc != 2) {
        cout << "USAGE: a.out DIRPATH" << endl;
        return -1;
    }
    string path(argv[1]);
    vector<string> filenames;
    filenames = getFiles(path);
    ofstream fout;
    fout.open("res.txt");
    for (int i = 0; i < filenames.size(); ++i) {
        string f = filenames[i];
        string fn = path + "\\\\" + f;
        char *filePath = (char *)malloc(sizeof(char) * (strlen(fn.c_str()) + 1));
        strcpy(filePath, fn.c_str());
        //cout << filePath << endl;
        Image img(filePath);
        tuple<float, float, float> res = img.getAverageHSV();
        fout << f << "," << get<0>(res) << "," << get<1>(res) << "," << get<2>(res) << endl;
    }
    fout.close();
    return 0;
}
