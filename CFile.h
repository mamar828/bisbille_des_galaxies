// #ifndef CFILE_H
// #define CFILE_H

#include <string>

class CFile {
public:
    CFile(const std::string &filename);
    ~CFile();

    bool Open();
    void Close();
    std::string Read();
    bool Write(const std::string &data);

private:
    std::string m_filename;
    FILE *m_file;
};

// #endif // CFILE_H
