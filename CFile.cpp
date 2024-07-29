#include "CFile.h"
#include <iostream>

CFile::CFile(const std::string &filename) : m_filename(filename), m_file(nullptr) {}

CFile::~CFile() {
    if (m_file) {
        Close();
    }
}

bool CFile::Open() {
    m_file = fopen(m_filename.c_str(), "r+");
    if (!m_file) {
        m_file = fopen(m_filename.c_str(), "w+");
    }
    return m_file != nullptr;
}

void CFile::Close() {
    if (m_file) {
        fclose(m_file);
        m_file = nullptr;
    }
}

std::string CFile::Read() {
    if (!m_file) return "";

    std::string content;
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), m_file)) {
        content += buffer;
    }
    return content;
}

bool CFile::Write(const std::string &data) {
    if (!m_file) return false;
    if (fputs(data.c_str(), m_file) == EOF) {
        return false;
    }
    return true;
}
