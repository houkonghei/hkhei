#include <iostream>

using namespace std;

int n;
int path[15]; // 用於記錄當前拆分的數字路徑，n <= 10，數組大小15足夠

// sum: 當前已拆分數字的和
// last: 上一個拆分的數字（保證後續數字不大於當前數字，實現非遞減，避免重複）
// depth: 當前路徑的深度（即拆分出了幾個數字）
void dfs(int sum, int last, int depth) {
    // 邊界條件：如果當前和等於 n，說明找到了一組滿足條件的拆分
    if (sum == n) {
        for (int i = 0; i < depth; ++i) {
            cout << path[i];
            if (i < depth - 1) {
                cout << "+";
            }
        }
        cout << endl;
        return;
    }

    // 從 last 開始枚舉下一個加數，保證大於等於 last 且嚴格小於 n
    for (int i = last; i < n; ++i) {
        if (sum + i <= n) {
            path[depth] = i;        // 記錄當前拆分的數字
            dfs(sum + i, i, depth + 1); // 遞歸進入下一層
        } else {
            break; // 如果求和已經超過 n，後續更大的 i 也不可能滿足，直接剪枝
        }
    }
}

int main() {
    // 讀入待拆分的自然數 n
    if (cin >> n) {
        // 從和為 0，最小加數為 1，深度為 0 開始深搜
        dfs(0, 1, 0);
    }
    return 0;
}
