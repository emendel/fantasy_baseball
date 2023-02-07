#include <iostream>
#include <vector>
#include <algorithm>
#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <list>
#include <deque>

using namespace std;

struct Player {
int dollars;
int valueops;
string name;
};
int SALARY_CAP = 21;
int MAX_POINTS = -1;
deque<Player> BEST_TEAM;

void branchAndBound(deque<Player> start, deque<Player> remaining, int salary, int points, int depth) {
    cout << "new time in branch and bound" << start.size() << endl;
    // cout << "in here" << endl;
    if (depth == 2) {
        // cout << "IN DEPTH" << endl;\
        // cout << "points: " << points << endl;
        if (points > MAX_POINTS && salary <= SALARY_CAP) {
            MAX_POINTS = points;
            BEST_TEAM = start;
            for (int i = 0; i < BEST_TEAM.size(); ++i){
                cout << BEST_TEAM[i].name;
            }
            cout << endl;
        }
        return;
    }

    for (int i = 0; i < remaining.size(); i++) {
        if (salary + remaining[i].dollars > SALARY_CAP) {
            continue;
        }
        int d  = remaining[i].dollars;
        int v = remaining[i].valueops;
        deque <Player> new_s;
        deque <Player> new_r;
        for (int j = 0; j < start.size(); j++){
            cout << start[i].name << endl;
            new_s.push_back(start[i]);
        }
        for (int j = 0; j < remaining.size(); j++){
            new_r.push_back(remaining[j]);
        }
        new_s.push_back(remaining[i]);

        new_r.pop_front();
        branchAndBound(new_s, new_r, salary + d, points + v, depth + 1);
    }
}

deque<Player> findBestTeam(deque<Player> &df) {
deque <Player> p;
branchAndBound(p, df, 0, 0, 0);
return BEST_TEAM;
}

deque<deque<string> > readCSV(const string &fileName) {
  ifstream file(fileName);
  deque<deque<string> > data;

  if (file.is_open()) {
    string line;
    while (getline(file, line)) {
      deque<string> row;
      string cell;
      istringstream lineStream(line);
      while (getline(lineStream, cell, ',')) {
        row.push_back(cell);
      }
      data.push_back(row);
    }
    file.close();
  }

  return data;
}

int main() {
    deque<deque<string> > data = readCSV("output.csv");
    deque<Player> df;

    for (int i = 1; i < data.size(); ++i){
        Player p = Player();
        p.name = data[i][2];
        p.valueops = stoi(data[i][25]);
        p.dollars = stoi(data[i][26]);
        df.push_back(p);
    }
    cout << df.size() << endl;

    deque<Player> bestTeam = findBestTeam(df);
    cout << bestTeam.size() << endl;
    for (int i = 0; i < bestTeam.size(); i++) {
        cout << bestTeam[i].name << endl;
    }

    return 0;
}