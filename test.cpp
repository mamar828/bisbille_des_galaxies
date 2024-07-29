//#include <CFile.h>
#include <stdafx.h>
#include <iostream>

using namespace std;

CFile m_File;

int bResult = m_File.Open(_T("\\\\.\\pipe\\pipe_beamage"), CFile::modeReadWrite);

if (bResult) AfxMessageBox(_T("File opened"));
else		 AfxMessageBox(_T("File NOT opened"));

m_bOpenPipe = 1;

cout << "Hello world" << endl;
