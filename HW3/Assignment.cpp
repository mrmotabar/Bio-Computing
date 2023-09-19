#include <bits/stdc++.h>
#include <ctime>
#include <random>
#include <fstream>

using namespace std;

const int n = 200, ant_t = 500;
const long double ro = 0.4, alpha = 0.7, beta = 0.9;
int adj[n][n], gen_t;
pair <int, int[n]> opt, ant[ant_t];
vector <int> permu[ant_t], permu_init;
long double pheromone[n][n], mu[n][n];
string file_number;


void read_input()
{
    ifstream input;
    input.open("job" + file_number + ".assign");
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            input >> adj[i][j];
        }
    }
}


void prep()
{
    opt.first = 1e7;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            pheromone[i][j] = 1;
        }
    }
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            mu[i][j] = (long double)1.0 / (adj[i][j] * adj[i][j]);
        }
    }
    for (int i = 0; i < n; i++)
    {
        permu_init.push_back(i);
    }
    for (int i = 0; i < ant_t; i++)
    {
        permu[i] = permu_init;
    }
}


void move_ants(int ind)
{
    vector <long double> prop;
    default_random_engine generator (time(0));
    for (int i = 0; i < ant_t; i++)
    {
        /*cout << i << endl;
        for (int u: permu[i])
        {
            cout << u << " ";
        }
        cout << endl;*/
        prop.clear();
        long double sigma = 0;
        for (int j = 0; j < permu[i].size(); j++)
        {
            double d = pow(pheromone[ind][permu[i][j]], alpha) * pow(mu[ind][permu[i][j]], beta);
            prop.push_back(d);
            sigma += d;
        }
        for (int j = 0; j < prop.size(); j++)
        {
            prop[j] /= sigma;
        }
        /*for (int j = 0; j < prop.size(); j++)
        {
            cout << prop[j] << " ";
        }
        cout << endl;*/
        discrete_distribution<int> distribution (prop.begin(),prop.end());
        int choosen = distribution(generator);
        //cout << "-->" << choosen << endl;
        ant[i].second[ind] = permu[i][choosen];
        permu[i].erase(permu[i].begin() + choosen);
        ant[i].first += adj[ind][ant[i].second[ind]];
    }
}


void upd_pheromones()
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            pheromone[i][j] *= ((long double)1.0 - ro);
        }
    }
    for (int i = 0; i < ant_t; i++)
    {
        for (int j = 0; j < n; j++)
        {
            pheromone[j][ant[i].second[j]] += ((long double)10.0 / ant[i].first); 
        }
    }
}


void upd_opt()
{
    for (int i = 0; i < ant_t; i++)
    {
        if (ant[i].first < opt.first)
        {
            opt.first = ant[i].first;
            memcpy(opt.second, ant[i].second, sizeof(opt.second));
            cout << opt.first << endl;
        }
        ant[i].first = 0;
        permu[i] = permu_init;
    }
}


int main()
{
    srand(time(0));
    cout << "please enter number of the file" << endl;
    cin >> file_number;
    read_input();
    cout << "please enter number of generations" << endl;
    cin >> gen_t;

    prep();
    while (gen_t--)
    {
        for (int i = 0; i < n; i++)
        {
            move_ants(i);
        }
        upd_pheromones();
        upd_opt();
        if (gen_t % 50 == 0)
        {
            cout << "---> " << opt.first <<endl;
        }
    }
    cout << endl << opt.first << endl;
    for (int i = 0; i < n; i++)
    {
        cout << opt.second[i] << " ";
    }
}
