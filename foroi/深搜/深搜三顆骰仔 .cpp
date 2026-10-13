#include <iostream>

using namespace std;

int path[4];

void dfs(int s,int i,int x)
{ if (x==3) 
  {  cout<<s<<":"<<path[0]<<path[1]<<path[2]<<endl;
     return;
  }
  else
  { for (int i=1;i<=6;i++)       {  
	     {path[x]=i;         
	     dfs(s+i,i,x+1);  }
  }
}

}

int main()
{  dfs(0,0,0);
}
