#include <bits/stdc++.h>
#include <ctime>
#include <random>
#include <fstream>

using namespace std;

string file_name;
const int size_of_society = 1000;
int node;
double **adj;
vector<int> selected;
vector<pair<double, int*>> society, child;
pair<double, int*> best_ans;

void read_input(string file_name)
{
    double *x, *y;
    ifstream input;
    input.open(file_name);
    if (file_name == "bayg29.tsp")
    {
        node = 29;
        adj = new double*[node];
        for (int i = 0; i < node; i++)
        {
            adj[i] = new double[node];
        }
        for (int i = 0; i < node - 1; i++)
        {
            for (int j = i + 1; j < node; j++)
            {
                input >> adj[i][j];
                adj[j][i] = adj[i][j];
            }
        }
    }
    else if (file_name == "gr229.tsp")
    {
        node = 229;
        x = new double[229];
        y = new double[229];
        adj = new double*[node];
        for (int i = 0; i < node; i++)
        {
            adj[i] = new double[node];
        }
        int c;
        for (int i = 0; i < node; i++)
        {
            input >> c >> x[i] >> y[i];
        }
        for (int i = 0; i < node; i++)
        {
            for (int j = i + 1; j < node; j++)
            {
                adj[i][j] = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
                adj[j][i] = adj[i][j];
            }
        }
    }
    else if (file_name == "pr1002.tsp")
    {
        node = 1002;
        x = new double[1002];
        y = new double[1002];
        adj = new double*[node];
        for (int i = 0; i < node; i++)
        {
            adj[i] = new double[node];
        }
        int c;
        for (int i = 0; i < node; i++)
        {
            input >> c >> x[i] >> y[i];
        }
        for (int i = 0; i < node; i++)
        {
            for (int j = i + 1; j < node; j++)
            {
                adj[i][j] = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
                adj[j][i] = adj[i][j];
            }
        }
    }
}

void make_society()
{
    for (int i = 0; i < size_of_society; i++)
    {
        society.push_back({0, new int[node - 1]});
        for (int j = 0; j < node - 1; j++)
        {
            society[i].second[j] = j + 1;
        }
        random_shuffle(society[i].second, society[i].second + node - 1);
    }
}

void cal_fit()
{
    for (int i = 0; i < society.size(); i++)
    {
        society[i].first = adj[0][society[i].second[0]];
        for(int j = 1; j < node - 1; j++)
        {
            society[i].first += adj[society[i].second[j - 1]][society[i].second[j]];
        }
        society[i].first += adj[society[i].second[node - 2]][0];
    }
}

void select_for_crossover()
{
    const int howmany_select = 30;
    int s1, s2;
    for (int i = 0; i < howmany_select; i++)
    {
        s1 = rand() % int(society.size());
        s2 = rand() % int(society.size());
        if (society[s1].first < society[s2].first)
        {
            selected.push_back(s1);
        }
        else
        {
            selected.push_back(s2);
        }
    }
}

void crossover()
{
    for (int i = 0; i < selected.size(); i++)
    {
        for (int j = 0; j < selected.size(); j++)
        {
            if (i != j)
            {
                child.push_back({0, new int[node - 1]});
                int ind1, ind2;
                bool isin[node];
                memset(isin, 0, node);
                ind1 = rand() % (node - 1);
                ind2 = rand() % (node - 1);
                if(ind1 > ind2)
                {
                    swap(ind1, ind2);
                }
                for (int k = ind1; k <= ind2; k++)
                {
                    child[child.size() - 1].second[k] = society[i].second[k];
                    isin[child[child.size() - 1].second[k]] = 1;
                }
                int ind = (ind2 + 1) % (node - 1);
                for (int k = ind2 + 1; k < node - 1; k++)
                {
                    if (!isin[society[j].second[k]])
                    {
                        child[child.size() - 1].second[ind] = society[j].second[k];
                        isin[child[child.size() - 1].second[ind]] = 1;
                        ind = (ind + 1) % (node - 1);
                    }
                }
                for (int k = 0; k <= ind2; k++)
                {
                    if (!isin[society[j].second[k]])
                    {
                        child[child.size() - 1].second[ind] = society[j].second[k];
                        isin[child[child.size() - 1].second[ind]] = 1;
                        ind = (ind + 1) % (node - 1);
                    }
                }
            }
        }
    }
}

void mutation()
{
    const int p1 = 40, p2 = 20;
    for (int i = 0; i < child.size(); i++)
    {
        int x = rand() % 100;
        if (x < p1)
        {
            int ind1, ind2;
            ind1 = rand() % (node - 1);
            ind2 = rand() % (node - 1);
            if(ind1 > ind2)
            {
                swap(ind1, ind2);
            }
            random_shuffle(child[i].second + ind1, child[i].second + ind2 + 1);
        }
        else if(x < p1 + p2)
        {
            int ind1, ind2;
            ind1 = rand() % (node - 1);
            ind2 = rand() % (node - 1);
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
    for (int i = 0; i < child.size(); i++)
    {
        child[i].first = adj[0][child[i].second[0]];
        for(int j = 1; j < node - 1; j++)
        {
            child[i].first += adj[child[i].second[j - 1]][child[i].second[j]];
        }
        child[i].first += adj[child[i].second[node - 2]][0];
    }
}

void replace()
{
    sort(child.begin(), child.end());
    sort(society.begin(), society.end());
    if(best_ans.first > society[0].first)
    {
        best_ans = society[0];
        cout << best_ans.first << endl;
    }
    if(best_ans.first > child[0].first)
    {
        best_ans = child[0];
        cout << best_ans.first << endl;
    }
    for (int i = 500; i < 1000; i++)
    {
        delete[] society[i].second;
        delete[] child[i].second;
    }
    for (int i = 500; i < society.size(); i++)
    {
        society[i] = child[i - 500];
    }
    child.clear();
    selected.clear();
}

double check(int* a, int length)
{
    double sum = 0;
    int last = 0;
    for (int i = 0; i < length; i++)
    {
        sum += adj[last][a[i]];
        last = a[i];
    }
    sum += adj[0][last];
    return sum;
}

int main()
{
    srand(time(0));
    cout << "please enter file name" << endl;
    cin >> file_name;
    read_input(file_name);
    make_society();
    cal_fit();
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
        replace();
    }
    cout << best_ans.first << endl;
    for (int i = 0; i < node - 1; i++)
    {
        cout << best_ans.second[i] << " ";
    }
    cout << endl;
    cout << check(best_ans.second, node - 1) << endl;
}