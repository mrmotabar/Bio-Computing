#include <bits/stdc++.h>
#include <ctime>
#include <random>
#include <fstream>

using namespace std;

const int size_of_society = 500;
const int select_crossover = 10;
const int size_of_child = select_crossover * (select_crossover - 1);
const int select_replace = 450;
const int n = 300;
vector<int> selected;
pair<int, int[n]> society[size_of_society], child[size_of_child];
pair<int, int[n]> best_ans;


void make_society()
{
    for (int i = 0; i < size_of_society; i++)
    {
        //society[i] = {0, new int[n]};
        for (int j = 0; j < n; j++)
        {
            society[i].second[j] = j;
        }
        random_shuffle(society[i].second, society[i].second + n);
    }
}


int cal_fit(int *arr)
{
    int ret = 0;
    int r1[2 * n - 1], r2[2 * n - 1];
    memset(r1, 0, sizeof(r1));
    memset(r2, 0, sizeof(r2));
    for (int i = 0; i < n; i++)
    {
        ret += r1[arr[i] + i];
        r1[arr[i] + i]++;
        ret += r2[n - 1 - i + arr[i]];
        r2[n - 1 - i + arr[i]]++;
    }
    return ret;
}


void cal_fit_society()
{
    for (int i = 0; i < size_of_society; i++)
    {  
        society[i].first = cal_fit(society[i].second);
    }
}


void race_select(pair<int, int[n]> *arr, int sz)
{
    int s1, s2;
    s1 = rand() % int(sz);
    s2 = rand() % int(sz);
    if (arr[s1].first < arr[s2].first)
    {
        selected.push_back(s1);
    }
    else
    {
        selected.push_back(s2);
    }
}


void select_for_crossover()
{
    selected.clear();
    for (int i = 0; i < select_crossover; i++)
    {
        race_select(society, size_of_society);
    }
}


void crossover()
{
    int cnt = 0;
    for (int i = 0; i < selected.size(); i++)
    {
        for (int j = 0; j < selected.size(); j++)
        {
            if (i != j)
            {
                //child[cnt] = {0, new int[n - 1]};
                int ind1, ind2;
                bool isin[n];
                memset(isin, 0, n);
                ind1 = rand() % n;
                ind2 = rand() % n;
                if(ind1 > ind2)
                {
                    swap(ind1, ind2);
                }
                for (int k = ind1; k <= ind2; k++)
                {
                    child[cnt].second[k] = society[i].second[k];
                    isin[child[cnt].second[k]] = 1;
                }
                int ind = (ind2 + 1) % n;
                for (int k = ind2 + 1; k < n; k++)
                {
                    if (!isin[society[j].second[k]])
                    {
                        child[cnt].second[ind] = society[j].second[k];
                        isin[child[cnt].second[ind]] = 1;
                        ind = (ind + 1) % n;
                    }
                }
                for (int k = 0; k <= ind2; k++)
                {
                    if (!isin[society[j].second[k]])
                    {
                        child[cnt].second[ind] = society[j].second[k];
                        isin[child[cnt].second[ind]] = 1;
                        ind = (ind + 1) % n;
                    }
                }
                cnt++;
            }
        }
    }
}


void mutation()
{
    const int p1 = 25, p2 = 15;
    for (int i = 0; i < size_of_child; i++)
    {
        int x = rand() % 100;
        if (x < p1)
        {
            int ind1, ind2;
            ind1 = rand() % n;
            ind2 = rand() % n;
            if(ind1 > ind2)
            {
                swap(ind1, ind2);
            }
            random_shuffle(child[i].second + ind1, child[i].second + ind2 + 1);
        }
        else if(x < p1 + p2)
        {
            int ind1, ind2;
            ind1 = rand() % n;
            ind2 = rand() % n;
            if(ind1 > ind2)
            {
                swap(ind1, ind2);
            }
            for (int j = ind1; j < ceil((ind1 + ind2) / 2); j++)
            {
                swap(child[i].second[j], child[i].second[ind2 - (j - ind1)]);
            }
        }
    }
}


void cal_fit_child()
{
    for (int i = 0; i < size_of_child; i++)
    {  
        child[i].first = cal_fit(child[i].second);
    }
}


void local_search()
{
    int p = 40;
    for(int i = 0; i < size_of_child; i++)
    {
        int x = rand() % 100;
        if(x < p)
        {
            int temp1[n], temp2[n], ans[n];
            int f_temp1, f_temp2, f_ans = 1e7;
            memcpy(temp1, child[i].second, sizeof(temp1));
            memcpy(temp2, child[i].second, sizeof(temp2));
            int t = n / 20;
            while (t--)
            {
                int x = temp1[0];
                for (int k = 0; k < n - 1; k++)
                {
                    temp1[k] = temp1[k + 1];
                }
                temp1[n - 1] = x;
                f_temp1 = cal_fit(temp1);
                if (f_temp1 < f_ans)
                {
                    f_ans = f_temp1;
                    memcpy(ans, temp1, sizeof(temp1));
                }
            }
            t = n / 20;
            while (t--)
            {
                int x = temp2[n - 1];
                for (int k = n - 1; k >= 0; k--)
                {
                    temp2[k] = temp2[k - 1];
                }
                temp2[0] = x;
                f_temp2 = cal_fit(temp1);
                if (f_temp2 < f_ans)
                {
                    f_ans = f_temp2;
                    memcpy(ans, temp2, sizeof(temp2));
                }
            }
            child[i].first = f_ans;
            memcpy(child[i].second, ans, sizeof(ans));
        }
    }
}


void replace()
{
    pair<int, int[n]> temp[size_of_society];
    selected.clear();
    for (int i = 0; i < select_replace; i++)
    {
        race_select(society, size_of_society);
    }
    for (int i = 0; i < select_replace; i++)
    {
        temp[i].first = society[selected[i]].first;
        memcpy(temp[i].second, society[selected[i]].second, sizeof(society[selected[i]].second));
    }
    selected.clear();
    for (int i = 0; i < size_of_society - select_replace; i++)
    {
        race_select(child, size_of_child);
    }
    for (int i = 0; i < selected.size(); i++)
    {
        temp[select_replace + i].first = child[selected[i]].first;
        memcpy(temp[select_replace + i].second, child[selected[i]].second, sizeof(child[selected[i]].second));
    }
    for (int i = 0; i < size_of_society; i++)
    {
        society[i].first = temp[i].first;
        memcpy(society[i].second, temp[i].second, sizeof(temp[i].second));
    }
    for (int i = 0; i < size_of_society; i++)
    {
        if (society[i].first < best_ans.first)
        {
            best_ans.first = society[i].first;
            memcpy(best_ans.second, society[i].second, sizeof(society[i].second));
        }
    }
    
}


int cal_fit_n2(int *arr)
{
    int ret = 0;
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (j - i == abs(arr[j] - arr[i]))
            {
                ret++;
            }
        }
    }
    return ret;
}


void draw()
{
    ofstream f;
    f.open("ans300.txt");
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < 2 * n; j++)
        {
            f << '-';
        }
        f << endl;
        for (int j = 0; j < n; j++)
        {
            if (i == n - 1 - best_ans.second[j])
            {
                f << '|' << '1';
            }
            else{
                f << '|' << ' ';
            }
        }
        f << '|' << endl;
    }
    for (int j = 0; j < 2 * n; j++)
    {
        f << '-';
    }
}


int main()
{
    srand(time(0));
    make_society();
    cal_fit_society();
    int tg = 5000;
    best_ans.first = 1e7;
    cout << "please enter number of generations" << endl;
    cin >> tg;
    while (tg--)
    {
        select_for_crossover();
        crossover();
        mutation();
        cal_fit_child();
        local_search();
        replace();
        if (tg % 1000 == 0)
        {
            cout << best_ans.first << endl;
        }
    }
    cout << best_ans.first << endl;
    for (int i = 0; i < n; i++)
    {
        cout << best_ans.second[i] << " ";
    }
    cout << endl;
    cout << cal_fit_n2(best_ans.second);
    draw();
}