#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <fstream>

using std::cout;
using std::cin;
using std::endl;

int main(int argc, char** argv)
{
    double x0; // initial horizontal position
    double v0; // initial launch speed
	double k; // spring constant
    double b; // drag coefficient
    double m; // object mass
	double alpha; // alpha = k/m
	double beta; // beta = b/m
    double minT = 0.0; // start at t=0
    double maxT; // end time
    double dt = 0.001; // time increment
    int steps; // stores number of time steps
    std::ifstream params; // file containing input parameters
    std::ofstream position; // file containing position solution
    double* tvals; // array to store time values
    double* xoft; // array to store horizontal position
    
    // open parameter file
    params.open("params");
    if(!params.is_open())
    {
        cout << "params stream failed to open!" << endl;
        return EXIT_FAILURE;
    }
    //else
        //cout << "params stream opened successfully." << endl;
    
    params >> x0;
    params >> v0;
	params >> k;
    params >> b;
    params >> m;
    params >> maxT;
    
    params.close(); // close parameter file
	
	alpha = k/m;
	beta = b/m;
    
    // calculate number of time steps
    steps = std::lround((maxT-minT)/dt+1);
    
    // allocate memory for time and velocity arrays
    tvals = new double[steps];
    xoft = new double[steps];
    
    // set initial conditions for time and velocity
    tvals[0] = minT;
	tvals[1] = minT+dt;
    xoft[0] = x0;
	xoft[1] = x0 + v0 * dt + 0.5 * (-alpha * x0 - beta * v0) * pow(dt,2);
    
    // solve for position
    for(int i=2; i<steps; i++)
    {
        tvals[i] = tvals[i-1] + dt;
        xoft[i] = (2.0-alpha*pow(dt,2))*xoft[i-1]/(1+beta*dt/2.0)+(beta*dt/2.0-1.0)*xoft[i-2]/(beta*dt/2.0+1.0);
    }
    
    // open solution file
    position.open("position.dat");
    if(!position.is_open())
    {
        cout << "position stream failed to open!" << endl;
        return EXIT_FAILURE;
    }
    //else
        //cout << "position stream opened successfully." << endl;
    
    // save initial values to solution file
    position << std::setprecision(10); // changes number of decimal places used
    
    // solve for position
    for(int i=0; i<steps; i++)
    {
        position << tvals[i] << "\t" << xoft[i] << endl;
    }
    
    position.close(); // close solution file
    
    // deallocate memory for arrays
    delete[] tvals;
    delete[] xoft;
    
	return EXIT_SUCCESS;
}
