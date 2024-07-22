/////////////////////////////////////////////////////////////////////////////////////////////////////////
// This configuration file was generated by the OAT/OAM Configurator at https://config.openastrotech.com
// and is for firmware to be used on a OpenAstroTracker.
// Save this as Configuration_local.hpp in the folder where you placed the firmware code.
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// Unique ConfigKey: TR:OAT,FWT:L,SL:N,HS:N,BD:M21,RST:N9,RDO:TU,RATP1500:O80:A6000:V1800:S16:T256:,RTR:Y,RT:1,DS:N9,DDT:TU,DATP1500:O80:A5000:V1800:S16:T256:,DT:1,DLIN120:D35:,STL:N,DY:NO,GP:N,LM:N,FC:Y,FS:BY,FD:TU,FAP150:O100:S1:H10:,FMSA600:V400:,APT:Y,AV:2,ZST:N8,ZD:TU,ZAP2000:O60:S16:H10:,ZAO:Y,LST:N8,LD:TU,LAP2000:O60:S16:H10:,LAO:N,RAH:N
/////////////////////////////////////////////////////////////////////////////////////////////////////////


#define NEW_STEPPER_LIB

#define NORTHERN_HEMISPHERE 1

// We are using the MKS GEN L V2.1 board
#if defined(BOARD) && BOARD != BOARD_AVR_MKS_GEN_L_V21
    #error Selected PIO environment does not match this configuration
#else
    #define BOARD BOARD_AVR_MKS_GEN_L_V21
#endif

////////////////////////////////
// RA Stepper configuration (OAT)
// See supported stepper values. Change according to the steppers you are using
// Using the NEMA 17, 0.9°/step stepper for RA
#define RA_STEPPER_TYPE STEPPER_TYPE_ENABLE
#define RA_DRIVER_TYPE DRIVER_TYPE_TMC2209_UART

// Define some RA stepper motor settings
#define RA_MOTOR_CURRENT_RATING        1500 // mA
#define RA_OPERATING_CURRENT_SETTING   80 // %
#define RA_STEPPER_ACCELERATION        6000
#define RA_STEPPER_SPEED               1800
#define RA_SLEW_MICROSTEPPING          16
#define RA_TRACKING_MICROSTEPPING      256
#define RA_INVERT_DIR                  1
#define RA_PULLEY_TEETH                16
#define RA_UART_STEALTH_MODE           0

#ifdef NEW_STEPPER_LIB
  #define RA_SLEWING_ACCELERATION_DEG  6.0  // deg/s/s
  #define RA_SLEWING_SPEED_DEG         6.0  // deg/s
#endif

// Track immediately after boot
#define TRACK_ON_BOOT 0

// Define limits for RA... 
#define RA_LIMIT_LEFT     5.5f
#define RA_LIMIT_RIGHT    6.5f
#define RA_TRACKING_LIMIT 6.75f // can't quite get to 7h...

////////////////////////////////
// DEC Stepper configuration 
// See supported stepper values. Change according to the steppers you are using
// Using the NEMA 17, 0.9°/step stepper for DEC
#define DEC_STEPPER_TYPE STEPPER_TYPE_ENABLE
#define DEC_DRIVER_TYPE DRIVER_TYPE_TMC2209_UART

// Define some DEC stepper motor settings
#define DEC_MOTOR_CURRENT_RATING        1500 // mA
#define DEC_OPERATING_CURRENT_SETTING   80 // %
#define DEC_STEPPER_ACCELERATION        5000
#define DEC_STEPPER_SPEED               1800
#define DEC_SLEW_MICROSTEPPING          16
#define DEC_GUIDE_MICROSTEPPING         256
#define DEC_INVERT_DIR                  0
#define DEC_PULLEY_TEETH                16
#define DEC_UART_STEALTH_MODE           0

#ifdef NEW_STEPPER_LIB
  #define DEC_SLEWING_ACCELERATION_DEG  6.0  // degs/s/s
  #define DEC_SLEWING_SPEED_DEG         6.0  // deg/s
#endif

// Define DEC limits
#define DEC_LIMIT_UP   120 // degrees from Home
#define DEC_LIMIT_DOWN 35 // degrees from Home


#define DISPLAY_TYPE DISPLAY_TYPE_NONE
#define USE_GPS 0
#define USE_GYRO_LEVEL 0


////////////////////////////////
// Focuser configuration 
// Define whether to support a focusing stepper motor on E1 or not. Currently: Focuser stepper

// Using the NEMA 17, 1.8°/step stepper for FOC
#define FOCUS_STEPPER_TYPE STEPPER_TYPE_ENABLE
#define FOCUS_STEPPER_SPR 200.0f
#define FOCUS_DRIVER_TYPE DRIVER_TYPE_TMC2209_UART

// Define Focus stepper motor power settings
#define FOCUS_MOTOR_CURRENT_RATING      1000 // mA
#define FOCUS_OPERATING_CURRENT_SETTING 90 // %
#define FOCUS_MICROSTEPPING             8 // steps
#define FOCUSER_MOTOR_HOLD_SETTING      10 // %
#define FOCUS_UART_STEALTH_MODE         1 // silent?
#define FOCUSER_ALWAYS_ON               1
#define FOCUS_STEPPER_ACCELERATION      3000 
#define FOCUS_STEPPER_SPEED             1800 
 

////////////////////////////////
// AutoPA Addon configuration 
// Define whether we have the AutoPA add on or not. Currently: AutoPA is installed

#define AUTOPA_VERSION 2

// Using the NEMA 17, 1.8°/step stepper for AZ
#define AZ_STEPPER_TYPE STEPPER_TYPE_ENABLED
#define AZ_STEPPER_SPR 200.0f
#define AZ_DRIVER_TYPE DRIVER_TYPE_TMC2209_UART

// Define AZ stepper motor power settings
#define AZ_MOTOR_CURRENT_RATING         2000 // mA
#define AZ_OPERATING_CURRENT_SETTING    60 // %
#define AZ_MICROSTEPPING                16 // steps
#define AZ_MOTOR_HOLD_SETTING           20 // %
#define AZ_STEPPER_SPEED                1000
#define AZ_STEPPER_ACCELERATION         500
#define AZ_INVERT_DIR                   0
#define AZ_ALWAYS_ON                    1


///////////////////////////////
// AZ parameters will require tuning according to your setup

// If you have a custom solution involving a rod you can uncomment and use the next 3 lines for calculations
// #define AZ_CIRCUMFERENCE        (115 * 2 * 3.1515927) // the circumference of the circle where the movement is anchored
// #define AZ_ROD_PITCH            1.0f                  // mm per full rev of stepper
// #define AZIMUTH_STEPS_PER_REV   (AZ_CIRCUMFERENCE / AZ_ROD_PITCH * AZ_STEPPER_SPR * AZ_MICROSTEPPING)  // Steps needed to turn AZ 360deg

// If you have a belt drive solution, you can uncomment and use the next 2 lines for calculations
//#define AZ_CIRCUMFERENCE        (725)  // the circumference of the circle where the movement is anchored
//#define AZ_PULLEY_TEETH         16


// Using the NEMA 17, 1.8°/step stepper for ALT
#define ALT_STEPPER_TYPE STEPPER_TYPE_ENABLED
#define ALT_STEPPER_SPR 200.0f
#define ALT_DRIVER_TYPE DRIVER_TYPE_TMC2209_UART

// Define ALT stepper motor power settings
#define ALT_MOTOR_CURRENT_RATING        2000 // mA
#define ALT_OPERATING_CURRENT_SETTING   70 // %
#define ALT_MICROSTEPPING               16 // steps
#define ALT_MOTOR_HOLD_SETTING          10 // %
#define ALT_STEPPER_SPEED               2000
#define ALT_STEPPER_ACCELERATION        1000
#define ALT_INVERT_DIR                  0
#define ALT_ALWAYS_ON                   0

#define DEW_HEATER 1

#define USE_HALL_SENSOR_RA_AUTOHOME 0

#define DEBUG_LEVEL (DEBUG_NONE)
