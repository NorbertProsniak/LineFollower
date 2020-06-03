#include <webots/Robot.hpp>
// Added a new include file
#include <webots/Motor.hpp>
#include <webots/Camera.hpp>

#define TIME_STEP 32
#define camera_time_step 32

// All the webots classes are defined in the "webots" namespace

using namespace webots;

int main(int argc, char **argv) {
 Robot *robot = new Robot();

 // get the motor devices
 Motor *leftMotor = robot->getMotor("left wheel motor");
 Motor *rightMotor = robot->getMotor("right wheel motor");
 // set the target position of the motors
 leftMotor->setPosition(10.0);
 rightMotor->setPosition(8.0);
 
 Camera *frontCamera = robot->getCamera("camera");
 frontCamera->enable(32);

 while (robot->step(TIME_STEP) != -1);

 delete robot;

 return 0;
}
