import java.util.Properties
import java.io.FileInputStream

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.users.ffq_app"
    compileSdk = 34

    // ۱. منطق هوشمند خواندن متغیرهای ادمین از فایل local.properties
    val localProperties = Properties()
    val localPropertiesFile = rootProject.file("local.properties")
    if (localPropertiesFile.exists()) {
        localProperties.load(FileInputStream(localPropertiesFile))
    }

    val adminUser = localProperties.getProperty("ADMIN_USER") ?: "\"admin\""
    val adminPass = localProperties.getProperty("ADMIN_PASS") ?: "\"1234\""

    defaultConfig {
        applicationId = "com.users.ffq_app"
        minSdk = 24 // حداقل نسخه اندروید (اندروید 7)
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }

        // ۲. تزریق متغیرهای امنیتی به محیط پروژه
        buildConfigField("String", "ADMIN_USER", adminUser)
        buildConfigField("String", "ADMIN_PASS", adminPass)
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        compose = true
        // ۳. فعال‌سازی رسمی تولید کلاس BuildConfig برای امنیت رمز عبور
        buildConfig = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // کتابخانه‌های هسته اندروید
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")

    // پلتفرم کامپوز
    implementation(platform("androidx.compose:compose-bom:2023.08.00"))

    // کتابخانه‌های اصلی کامپوز
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")

    // *** کتابخانه‌های حیاتی برای رفع ارورهای شما ***

    // 1. برای رفع ارور Unresolved reference: viewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.0")

    // 2. برای آیکون‌های خاص (مثل آیکون چشم پسورد)
    implementation("androidx.compose.material:material-icons-extended:1.6.0")

    // 3. برای ذخیره و خواندن فایل‌های جیسون (Gson)
    implementation("com.google.code.gson:gson:2.10.1")

    // کتابخانه‌های تست (پیش‌فرض)
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2023.08.00"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}