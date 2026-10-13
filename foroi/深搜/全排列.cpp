#include <iostream>

using namespace std;

// 定義最大全排列的數字數量
int n;                // 使用者想要排列的數字個數 (1 到 n)
int path[10];      // 儲存當前的排列路徑
bool visited[10];  // 記錄數字是否已經被使用過

// DFS 遞迴函數
// u 代表當前正在填寫第幾個位置 (從 0 開始)
void dfs(int u) {
    // 遞迴終止條件：如果填滿了 n 個位置，代表找到一組全排列
    if (u == n) {
        for (int i = 0; i < n; ++i) {
            cout << path[i] << " ";
        }
        cout << "\n";
        return;
    }

    // 列舉所有可能的數字 (從 1 到 n)
    for (int i = 1; i <= n; ++i) {
        // 如果數字 i 還沒有被使用過
        if (!visited[i]) {
            path[u] = i;        // 1. 做出選擇：將數字 i 放到當前位置 u
            visited[i] = true;  // 2. 標記該數字已被使用

            dfs(u + 1);         // 3. 遞迴：繼續填寫下一個位置

            visited[i] = false; // 4. 回溯：將狀態復原，供其他分支使用
        }
    }
}

int main() {
    cout << "請輸入排列數字個數 n (1-" << 10 - 1 << "): ";
    cin>>n;

    // 初始化狀態陣列（C++98 手動初始化）
    for (int i = 0; i <10; ++i) {
        visited[i] = false;
    }

    cout << "--- 全排列結果 ---" << endl;
    dfs(0); // 從第 0 個位置開始填寫

    return 0;
}
