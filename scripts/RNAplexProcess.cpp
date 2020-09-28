#include <bits/stdc++.h>

using namespace std;

int MIN_INTERACTION = 8;

void getRange(const string& line, int& posStart, int& posEnd, int& start, int& end)
{
    while(line[posStart] == ' ') posStart++;

    posEnd = line.find(",", posStart+1);

    // find the first range
    start = stoi(line.substr(posStart, posEnd-posStart));
    posStart = posEnd;
    posEnd = line.find(" ", posStart+1);
    end = stoi(line.substr(posStart+1, posEnd-posStart));
}

map< pair<int, int>, int> getBoundRegion(const string& left, const string& right)
{
    map< pair<int, int>, int> bound;
    int i =0;
    int j = 0;
    int sLeft = 0;
    int sRight = 0;
    int count = 0;
    const int n = left.length();
    const int m = right.length();

    while(i<n, j<m)
    {
        if(left[i] == ')' && right[j] == ')')
        {
            count++;
            i++;
            j++;
        }
        else
        {
            if(count >= MIN_INTERACTION)
                bound[{sLeft, sRight}] = count;
            count = 0;
            while(left[i] != ')' && i<n) i++;
            while(right[j] != ')' && j<m) j++;
            sLeft = i;
            sRight = j;
        }
    }
    return bound;
}

void process(string& line)
{
    int pos;
    int posStart, posEnd;
    string tmp, left, right, test;
    int start, end, leftStart, leftEnd, rightStart, rightEnd;
    map< pair<int, int>, int> bound;
    map< pair<int, int>, int>::iterator it;

    // work with the dot profile
    posStart = line.find(" ");
    tmp = line.substr(0, posStart);
    pos = tmp.find("&");

    left = tmp.substr(0, pos);
    // reverse the left side for ease ** range counts from ligation part**
    string newLeft = "";
    for(int i=0;i<left.length();i++)
    {
        newLeft+= (left[i] == '(') ? ')' : '.';
    }
    reverse(newLeft.begin(), newLeft.end());

    right = tmp.substr(pos+1, tmp.length());

    // first range
    getRange(line, posStart, posEnd, start, end);

    leftStart = start;
    leftEnd = end;

    // find the second range
    posStart = line.find(":", posEnd+1);
    posStart++;
    getRange(line, posStart, posEnd, start, end);

    rightStart = start;
    rightEnd = end;

    // cout  << leftStart << "__" << leftEnd << "|" << rightStart << "__" << rightEnd << endl;
    // cout << newLeft << endl << right << endl << "--------------------" << endl;

    bound = getBoundRegion(newLeft, right);

    it = bound.begin();
    if(it == bound.end())
    {
        cout << endl;
        return;
    }
    while(it != bound.end())
    {
        // cout << "raw data: " << it->first.first << "|" << it->first.second << "\t" << it->second << endl;
        int startL = leftEnd - it->first.first - it->second;
        int startR = it->first.second + rightStart - 1;

        cout << startL << "," << it->second + startL << "|";
        cout << startR << "," << it->second + startR;

        it++;
        if(it != bound.end()) cout << ";";
        else cout << endl;
    }

}

int main()
{
    string line;
    int seqNum = 0;
    int linesPerQuery = 0;

    cout << "DG\tpos_in_interaction" << endl;

    while(getline(cin, line))
    {
        linesPerQuery++;
        switch (linesPerQuery)
        {
           // case 1: cout << line << "\t";
           case 1: line.erase(line.begin()); cout << line << "\t";
                   break;
           case 2: continue; //line.erase(line.begin()), cout << line << endl;
                    break;
           case 3: process(line);
                   break;
           default: linesPerQuery = 0; continue;
                    break;
        }
    }

    return 0;
}
