#include <bits/stdc++.h>
using namespace std;

void backtrack(vector <int> &path, int curri, int currj,int o)
{
    path.pop_back();

    int previ = path[path.size()-1]/16, prevj = path[path.size()-1]%16;

    if(previ == curri+1)
    {
        if(o==0) forward();
        else if(o==1) backward();
        else if(o==2) right();
        else if(o==3) left();
    }
    else if(previ == curri-1)
    {
        if(o==1) forward();
        else if(o==0) backward();
        else if(o==2) left();
        else if(o==3) right();
    }
    else if(prevj == currj+1)
    {
        if(o==2) forward();
        else if(o==3) backward();
        else if(o==1) right();
        else if(o==0) left();
    }
    else if(prevj == currj-1)
    {
        if(o==3) forward();
        else if(o==2) backward();
        else if(o==0) right();
        else if(o==1) left();
    }
}

int decideDirection(int i,int j,double r, double l,double c,vector<vector<bool>> &visited)
{
    int o = getOrient(); // 0=> facing down 1=>facing up 2=> facing right 3=> facing left

    if(j<=7 && i<=7) // priority right-down-top-left  // 2nd quadrant 
    {
        if(o==0)
        {
            if(l>0.15 && visited[i][j+1]==false) return -1;
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(r>0.15 && visited[i][j-1]==false) return 1;
            else backtrack(path,i,j,o);
        }
        else if(o==1)
        {
            if(l>0.15 && visited[i][j+1]==false) return -1;
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(r>0.15 && visited[i][j-1]==false) return 1;
            else backtrack(path,i,j,o);
        }
        else if(o==2)
        {
            if(l>0.15 && visited[i][j+1]==false) return -1;
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(r>0.15 && visited[i][j-1]==false) return 1;            
            else backtrack(path,i,j,o);
        }
        else if(o==3)
        {
            if(l>0.15 && visited[i][j+1]==false) return -1;            
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(r>0.15 && visited[i][j-1]==false) return 1;            
            else backtrack(path,i,j,o);
        }
    }
    else if(j>=8 && i<=7) // priority left-down-top-right  // 1st quadrant
    {
        if(o==0)
        {
            if(r>0.15 && visited[i][j-1]==false) return 1;            
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(l>0.15 && visited[i][j+1]==false) return -1;
            else backtrack(path,i,j,o);
        }
        else if(o==1)
        {
            if(l>0.15 && visited[i][j-1]==false) return -1;
            else if(c>0.15 && visited[i-1][j]==false) return 0;
            else if(r>0.15 && visited[i][j+1]==false) return 1;
            else backtrack(path,i,j,o);
        }
        else if(o==2)
        {
            if(r>0.15 && visited[i+1][j]==false) return 1;            
            else if(l>0.15 && visited[i-1][j]==false) return -1;
            else if(r>0.15 && visited[i][j+1]==false) return 0;            
            else backtrack(path,i,j,o);
        }
        else if(o==3)
        {
            if(c>0.15 && visited[i][j-1]==false) return 0;
            else if(l>0.15 && visited[i+1][j]==false) return -1;
            else if(r>0.15 && visited[i][j-1]==false) return 1;            
            else backtrack(path,i,j,o);
        }
    }
    else if(j<=7 && i>=8) // priority right-top-down-left  // 3rd quadrant
    {
        if(o==0)
        {
            if(l>0.15 && visited[i][j+1]==false) return -1;
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(r>0.15 && visited[i][j-1]==false) return 1;            
            else backtrack(path,i,j,o);
        }
        else if(o==1)
        {
            if(r>0.15 && visited[i][j+1]==false) return 1;            
            else if(c>0.15 && visited[i-1][j]==false) return 0;
            else if(l>0.15 && visited[i][j-1]==false) return -1;            
            else backtrack(path,i,j,o);
        }
        else if(o==2)
        {
            if(c>0.15 && visited[i][j+1]==false) return 0;            
            else if(l>0.15 && visited[i-1][j]==false) return -1;
            else if(r>0.15 && visited[i+1][j]==false) return 1;            
            else backtrack(path,i,j,o);
        }
        else if(o==3)
        {
            if(r>0.15 && visited[i-1][j]==false) return 1;            
            else if(l>0.15 && visited[i+1][j]==false) return -1;
            else if(c>0.15 && visited[i][j+1]==false) return 0;            
            else backtrack(path,i,j,o);
        }
    }
    else if(j>=8 && i>=8) // priority left-top-down-right  // 4th quadrant 
    {
        if(o==0)
        {
            if(r>0.15 && visited[i][j-1]==false) return 1;            
            else if(c>0.15 && visited[i+1][j]==false) return 0;
            else if(l>0.15 && visited[i][j+1]==false) return -1;            
            else backtrack(path,i,j,o);
        }
        else if(o==1)
        {
            if(l>0.15 && visited[i][j-1]==false) return -1;            
            else if(c>0.15 && visited[i-1][j]==false) return 0;
            else if(r>0.15 && visited[i][j+1]==false) return 1;            
            else backtrack(path,i,j,o);
        }
        else if(o==2)
        {
            if(l>0.15 && visited[i-1][j]==false) return -1;            
            else if(r>0.15 && visited[i+1][j]==false) return 1;
            else if(c>0.15 && visited[i][j+1]==false) return 0;            
            else backtrack(path,i,j,o);
        }
        else if(o==3)
        {
            if(c>0.15 && visited[i][j-1]==false) return 0;            
            else if(r>0.15 && visited[i-1][j]==false) return 1;
            else if(l>0.15 && visited[i+1][j]==false) return -1;            
            else backtrack(path,i,j,o);
        }
    }

    return 17; // a number different from 0,1,-1 , 17 => just stay there
}

int main()
{
    double r,l,c; //distance from the walls

    r = getr(); l = getl(); c = getc(); 

    double x,y; //positions (x,y)

    vector <vector<bool>> visited (16,vector<bool>(16,false)); 

    vector <int> path;

    while(true)
    {
        x = getx(); y = gety();    // x should be coloumns, y should be rows

        int i = (int)y, j = (int)x;

        visited[i][j] = true;

        path.push_back(i*16 + j);

        if((i==7 || i==8) && (j==7 || j==8)) break;

        int dirn = decideDirection(i,j,r,l,c,visited); //this we have to decide

        if(dirn==0) forward();
        else if(dirn==1) right();
        else if(dirn==-1) left();
        else if(dirn==17) path.pop_back(); // so that it is not entered twice
    }

    int n = path.size();

    for(int i = n-1;i>=1;i--)
    {
        int previ = path[i-1]/16, prevj = path[i-1]%16;

        if(previ == curri+1)
        {
            if(o==0) forward();
            else if(o==1) backward();
            else if(o==2) right();
            else if(o==3) left();
        }
        else if(previ == curri-1)
        {
            if(o==1) forward();
            else if(o==0) backward();
            else if(o==2) left();
            else if(o==3) right();
        }
        else if(prevj == currj+1)
        {
            if(o==2) forward();
            else if(o==3) backward();
            else if(o==1) right();
            else if(o==0) left();
        }
        else if(prevj == currj-1)
        {
            if(o==3) forward();
            else if(o==2) backward();
            else if(o==0) right();
            else if(o==1) left();
        }
    }

    for(int i = 0;i<n-1;i++)
    {
        int previ = path[i+1]/16, prevj = path[i+1]%16;

        if(previ == curri+1)
        {
            if(o==0) forward();
            else if(o==1) backward();
            else if(o==2) right();
            else if(o==3) left();
        }
        else if(previ == curri-1)
        {
            if(o==1) forward();
            else if(o==0) backward();
            else if(o==2) left();
            else if(o==3) right();
        }
        else if(prevj == currj+1)
        {
            if(o==2) forward();
            else if(o==3) backward();
            else if(o==1) right();
            else if(o==0) left();
        }
        else if(prevj == currj-1)
        {
            if(o==3) forward();
            else if(o==2) backward();
            else if(o==0) right();
            else if(o==1) left();
        }
    }
}