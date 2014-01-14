package org.rocket.testexe;

public class OpenRocketAPI
{
	public OpenRocketAPI() {}

        
        public int GetVelocityX() {
                return (int) Math.random();
        }
        
        public int GetVelocityY() {
                return (int) Math.random();
        }
        
        public int GetVelocityZ() {
                return (int) Math.random();
        }
        
        
        public int LoadRocket(String szFileName) {
                return 0;
        }
        
        public void RunSimulation() {
                
        };
        
        public double getMaxAltitude() {
                        return -1;
                }
        
        public double getMaxVelocity() {
                        return -1;
        }
        
        public double getMaxAcceleration() {
                        return -1;
        }
        
        public double getMaxMachNumber() {
                        return -1;
        }
        
        public double getTimeToApogee() {
                        return -1;
        }
        
        public double getFlightTime() {
                        return -1;
        }
        
        public double getGroundHitVelocity() {
                        return -1;
        }
        
        public double getLaunchRodVelocity() {
                        return -1;
        }
        
        public double getDeploymentVelocity() {
                        return -1;
        }
        
        
        private int loadorkfile(String filename) {
                return 1;
        }
        
}
