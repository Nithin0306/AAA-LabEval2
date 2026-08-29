#include <bits/stdc++.h>
using namespace std;

struct State {
    int room;
    int mask;
};

struct ParentInfo {
    int parentState;
    string action;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int r, d, s;
    int caseNo = 1;

    while (cin >> r >> d >> s) {
        if (r == 0 && d == 0 && s == 0)
            break;

        vector<vector<int>> doors(r);

        for (int i = 0; i < d; i++) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;

            doors[u].push_back(v);
            doors[v].push_back(u);
        }

        vector<vector<int>> switches(r);

        for (int i = 0; i < s; i++) {
            int u, v;
            cin >> u >> v;
            --u;
            --v;

            switches[u].push_back(v);
        }

        int initialMask = 1;
        int totalMasks = 1 << r;
        int totalStates = r * totalMasks;

        vector<vector<bool>> visited(
            r, vector<bool>(totalMasks, false)
        );

        vector<ParentInfo> parent(totalStates);

        queue<State> q;
        q.push({0, initialMask});
        visited[0][initialMask] = true;

        int finalState = -1;
        int goalMask = 1 << (r - 1);

        while (!q.empty()) {
            State current = q.front();
            q.pop();

            int room = current.room;
            int mask = current.mask;
            int currentState = room * totalMasks + mask;

            if (room == r - 1 && mask == goalMask) {
                finalState = currentState;
                break;
            }

            for (int target : switches[room]) {
                if (target == room)
                    continue;

                int newMask;

                if (mask & (1 << target))
                    newMask = mask & ~(1 << target);
                else
                    newMask = mask | (1 << target);

                int newState = room * totalMasks + newMask;

                if (!visited[room][newMask]) {
                    visited[room][newMask] = true;

                    string action;

                    if (mask & (1 << target))
                        action = "Switch off light in room ";
                    else
                        action = "Switch on light in room ";

                    action += to_string(target + 1) + ".";

                    parent[newState] = {
                        currentState,
                        action
                    };

                    q.push({room, newMask});
                }
            }

            for (int nextRoom : doors[room]) {
                if (!(mask & (1 << nextRoom)))
                    continue;

                int newState =
                    nextRoom * totalMasks + mask;

                if (!visited[nextRoom][mask]) {
                    visited[nextRoom][mask] = true;

                    parent[newState] = {
                        currentState,
                        "Move to room " +
                        to_string(nextRoom + 1) + "."
                    };

                    q.push({nextRoom, mask});
                }
            }
        }

        cout << "Villa #" << caseNo++ << '\n';

        if (finalState == -1) {
            cout << "The problem cannot be solved.\n\n";
            continue;
        }

        vector<string> path;
        int currentState = finalState;
        int startState = initialMask;

        while (currentState != startState) {
            path.push_back(parent[currentState].action);
            currentState = parent[currentState].parentState;
        }

        reverse(path.begin(), path.end());

        cout << "The problem can be solved in "
             << path.size() << " steps:\n";

        for (const string& action : path)
            cout << "- " << action << '\n';

        cout << '\n';
    }

    return 0;
}