#ifdef BOARD_OBP60S3

#include "Pagedata.h"
#include "OBP60Extensions.h"
#include "images/logo64.xbm"
#include <esp_clk.h>

/*
 * Special system page, called directly with fast key sequence 5,4
 * Out of normal page order.
 */

class PageSystem : public Page
{
uint64_t chipid;
bool simulation;
String env_sensor;
String buzzer_mode;
uint8_t buzzer_power;
String cpuspeed;

char mode = 'N'; // (N)ormal, (D)evice list

public:
    PageSystem(CommonData &common){
        commonData = &common;
        common.logger->logDebug(GwLog::LOG,"Instantiate PageSystem");
        chipid = ESP.getEfuseMac();
        simulation = common.config->getBool(common.config->useSimuData);
        env_sensor = common.config->getString(common.config->useEnvSensor);
        buzzer_mode = common.config->getString(common.config->buzzerMode);
        buzzer_power = common.config->getInt(common.config->buzzerPower);
        cpuspeed = common.config->getString(common.config->cpuSpeed);
        // useRTC off oder typ
        // useGPS off oder typ
    }

    virtual void setupKeys(){
        commonData->keydata[0].label = "EXIT";
        commonData->keydata[1].label = "MODE";
        commonData->keydata[2].label = "";
        commonData->keydata[3].label = "";
        commonData->keydata[4].label = "STBY";
        commonData->keydata[5].label = "ILUM";
    }

    virtual int handleKey(int key){
        // do *NOT* handle key #1 this handled by obp60task as exit

        // Switch display mode
        if (key == 2) {
            if (mode == 'N') {
                mode = 'D';
            } else {
                mode = 'N';
            }
            if (hasFRAM) fram.write(FRAM_VOLTAGE_MODE, mode);
            return 0;
        }
        // Code for keylock
        if (key == 11) {
            commonData->keylock = !commonData->keylock;
            return 0;
        }
        return key;
    }

    virtual void displayPage(PageData &pageData){
        GwConfigHandler *config = commonData->config;
        GwLog *logger = commonData->logger;

        // Get config data
        String flashLED = config->getString(config->flashLED);

        // Optical warning by limit violation (unused)
        if(String(flashLED) == "Limit Violation"){
            setBlinkingLED(false);
            setFlashLED(false); 
        }

        // Logging boat values
        LOG_DEBUG(GwLog::LOG,"Drawing at PageSystem");

        // Draw page
        //***********************************************************

        const uint16_t y0 = 120; // data table starts here

        // Set display in partial refresh mode
        getdisplay().setPartialWindow(0, 0, getdisplay().width(), getdisplay().height()); // Set partial update

        if (mode == 'N') {
            getdisplay().setFont(&Ubuntu_Bold12pt7b);
            getdisplay().setCursor(20, 50);
            getdisplay().print("System Information");

            getdisplay().setFont(&Ubuntu_Bold8pt7b);

            char ssid[23];
            snprintf(ssid, 23, "MCUDEVICE-%04X%08X", (uint16_t)(chipid >> 32), (uint32_t)chipid);
            getdisplay().setCursor(20, 70);
            getdisplay().print(ssid);
            getdisplay().setCursor(20, 100);
            getdisplay().print("Press STBY for white page and standby");

            getdisplay().setCursor(2, y0);
            getdisplay().print("Simulation:");
            getdisplay().setCursor(140, y0);
            getdisplay().print(simulation ? "on" : "off");

            getdisplay().setCursor(202, y0);
            getdisplay().print("Wifi:");
            getdisplay().setCursor(340, y0);
            getdisplay().print("on");

            getdisplay().setCursor(2, y0 + 16);
            getdisplay().print("Environment:");
            getdisplay().setCursor(140, y0 + 16);
            getdisplay().print(env_sensor);

            getdisplay().setCursor(2, y0 + 32);
            getdisplay().print("Buzzer:");
            getdisplay().setCursor(140, y0 + 32);
            getdisplay().print(buzzer_mode);

            getdisplay().setCursor(2, y0 + 48);
            getdisplay().print("CPU speed:");
            getdisplay().setCursor(140, y0 + 48);
            getdisplay().print(cpuspeed);
            getdisplay().print(" ");
            int cpu_freq = esp_clk_cpu_freq();
            getdisplay().print(String(cpu_freq));

            getdisplay().drawXBitmap(320, 25, logo64_bits, logo64_width, logo64_height, commonData->fgcolor);
        } else {
            // NMEA2000 device list
            getdisplay().setFont(&Ubuntu_Bold12pt7b);
            getdisplay().setCursor(20, 50);
            getdisplay().print("NMEA2000 device list");
        }

        // Update display
        getdisplay().nextPage();    // Partial update (fast)

    };
};

static Page* createPage(CommonData &common){
    return new PageSystem(common);
}

/**
 * with the code below we make this page known to the PageTask
 * we give it a type (name) that can be selected in the config
 * we define which function is to be called
 * and we provide the number of user parameters we expect
 * this will be number of BoatValue pointers in pageData.values
 */
PageDescription registerPageSystem(
    "System",   // Page name
    createPage, // Action
    0,          // No bus values
    true        // Headers are anabled so far
);

#endif
