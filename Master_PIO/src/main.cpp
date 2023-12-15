//Include libraries
#include <Arduino.h>
#include <esp_camera.h>
#include <SD.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include "SD_MMC.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

#include <iostream>
#include <fstream>
#include <string>
#include <SPIFFS.h>

#include "../models/model.h"

char preprocess[] = "min_max";


// Define camera pins
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// TensorFlow Lite model settings

constexpr int kTensorArenaSize = 3 * 1024  * 1024;
EXT_RAM_ATTR uint8_t* tensor_arena = nullptr;

// Declare the interpreter object here to make it accessible in both setup and loop
tflite::MicroMutableOpResolver<10> resolver;
tflite::MicroErrorReporter micro_error_reporter;
tflite::ErrorReporter* error_reporter = &micro_error_reporter;
tflite::MicroInterpreter* interpreter_ptr = nullptr;
TfLiteTensor* model_input = nullptr;


// Declare preprocessing function
void preprocessImageReloaded(uint8_t* raw_cam, float* normalized_cam){
    for(int i=0; i<(160*120); i++){
        float mean =  114.31817292906746;
        float standard_deviation = 77.30169303183406;
        float const min_value = 0;
        float const max_value = 255; 
        
        if (preprocess == "none")
        {
            normalized_cam[i] = raw_cam[i];
        } else if (preprocess == "zscore")
        {
            normalized_cam[i] = (raw_cam[i]-mean) / standard_deviation;
        } else if (preprocess == "min_max")
        {
            normalized_cam[i] = (raw_cam[i]-min_value) / (max_value - min_value);
        }

    }
}


void setup() {
    

    // Set the baud rate of the serial monitor to 115200
    Serial.begin(115200);
    Serial.println("Start");
    Serial.setDebugOutput(true);
    Serial.println("Oben");

    tensor_arena = new uint8_t[kTensorArenaSize];
    if(!tensor_arena) Serial.println("Failed to Allocate Tensor Arena");

    // Initialize camera
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_GRAYSCALE;

    if (psramFound()) {
        config.frame_size = FRAMESIZE_QQVGA;
        config.jpeg_quality = 10;
        config.fb_count = 2;
        Serial.println("PSRAM found");
    } else {
        config.frame_size = FRAMESIZE_QQVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
        Serial.println("PSRAM not found");
    }

    // Set other camera config parameters
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.println("Camera initialization failed!");
        return;
    }

     // Initialize the SD card
    if (!SD_MMC.begin()) {
        Serial.println("SD card initialization failed!");
        return;
    }
    // Load model data
   const tflite::Model* model = ::tflite::GetModel(model_data);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        TF_LITE_REPORT_ERROR(error_reporter,
      "Model provided is schema version %d not equal "
      "to supported version %d.\n",
      model->version(), TFLITE_SCHEMA_VERSION);
}
    // Add layers and functions needed for the CNN
    static tflite::MicroMutableOpResolver<7> micro_mutable_op_resolver;  
    micro_mutable_op_resolver.AddConv2D();
    micro_mutable_op_resolver.AddMaxPool2D();
    micro_mutable_op_resolver.AddReduceMax();
    micro_mutable_op_resolver.AddShape();
    micro_mutable_op_resolver.AddReshape();
    micro_mutable_op_resolver.AddGather();
    micro_mutable_op_resolver.AddFullyConnected();

    // Initialize Interpreter
    tflite::MicroInterpreter interpreter(model, micro_mutable_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);
    interpreter.AllocateTensors();
    
    // Capture image 
    camera_fb_t *fb = NULL;
    fb = esp_camera_fb_get();
    if (!fb) {
        Serial.println("Camera capture failed!");
        return;
    }
    // Process the captured image (convert to grayscale, resize, preprocess, etc.)
    float* normalized_cam_data = new float[160*120];
    preprocessImageReloaded(fb->buf, normalized_cam_data);

    // Set input tensor data (preprocess image)
    TfLiteTensor* input_tensor = interpreter.input(0);    
    for(int i=0; i<(120*160); i++){
        input_tensor->data.f[i] = normalized_cam_data[i];
    }
    //Perform prediction
    Serial.println("Performing Prediction...");
    interpreter.Invoke();
    TfLiteTensor* output = interpreter.output(0);
    float value = output->data.f[0];

    // Display prediction
    Serial.println("Predicted value: ");
    Serial.println(value);

    // Clean up
    esp_camera_fb_return(fb);
}

void loop() {

}