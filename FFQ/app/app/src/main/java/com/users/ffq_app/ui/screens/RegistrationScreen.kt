package com.users.ffq_app.ui.screens

import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.users.ffq_app.data.model.LocalAppStrings
import com.users.ffq_app.data.model.RegistrationData

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegistrationScreen(
    initialData: RegistrationData? = null,
    onNavigateBack: () -> Unit,
    onProceedToFFQ: (RegistrationData) -> Unit
) {
    val context = LocalContext.current
    val strings = LocalAppStrings.current

    var regData by remember { mutableStateOf(initialData ?: RegistrationData()) }

    // Section collapse states
    var isDemoExpanded by remember { mutableStateOf(true) }
    var isAnthroExpanded by remember { mutableStateOf(true) }
    var isSubstanceExpanded by remember { mutableStateOf(false) }
    var isMedsExpanded by remember { mutableStateOf(false) }
    var isMedicalExpanded by remember { mutableStateOf(false) }
    var isIpaqExpanded by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(strings.btnRegistration, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = strings.back)
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp)
                .verticalScroll(rememberScrollState())
        ) {
            Spacer(Modifier.height(8.dp))

            // 1. Demographics & Base Info
            SectionCard(
                title = "۱. اطلاعات هویتی و دموگرافیک",
                isExpanded = isDemoExpanded,
                onToggle = { isDemoExpanded = !isDemoExpanded }
            ) {
                OutlinedTextField(
                    value = regData.id,
                    onValueChange = { regData = regData.copy(id = it) },
                    label = { Text("کد بیمار / شناسه (ID) *") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))

                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = regData.age,
                        onValueChange = { regData = regData.copy(age = it) },
                        label = { Text("سن (Age)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                    OutlinedTextField(
                        value = regData.diagnosisMO,
                        onValueChange = { regData = regData.copy(diagnosisMO = it) },
                        label = { Text("ماه تشخیص (DiagnosisMO)") },
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(Modifier.height(12.dp))
                Text("جنسیت (Gender):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Row(Modifier.fillMaxWidth()) {
                    listOf("زن (0)" to 0, "مرد (1)" to 1).forEach { (label, value) ->
                        Row(
                            Modifier
                                .selectable(
                                    selected = (regData.gender == value),
                                    onClick = { regData = regData.copy(gender = value) },
                                    role = Role.RadioButton
                                )
                                .padding(horizontal = 8.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            RadioButton(selected = (regData.gender == value), onClick = null)
                            Text(text = label, modifier = Modifier.padding(start = 4.dp))
                        }
                    }
                }

                Spacer(Modifier.height(8.dp))
                Text("وضعیت تاهل (Marital):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Column {
                    listOf("مجرد (0)" to 0, "متأهل (1)" to 1, "مطلقه (2)" to 2, "بیوه (3)" to 3).chunked(2).forEach { rowList ->
                        Row(Modifier.fillMaxWidth()) {
                            rowList.forEach { (label, value) ->
                                Row(
                                    Modifier
                                        .weight(1f)
                                        .selectable(
                                            selected = (regData.marital == value),
                                            onClick = { regData = regData.copy(marital = value) },
                                            role = Role.RadioButton
                                        )
                                        .padding(vertical = 4.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    RadioButton(selected = (regData.marital == value), onClick = null)
                                    Text(text = label, modifier = Modifier.padding(start = 4.dp), fontSize = 13.sp)
                                }
                            }
                        }
                    }
                }

                Spacer(Modifier.height(8.dp))
                Text("تحصیلات (Education):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                val educations = listOf(
                    "بی‌سواد / ابتدایی (0)" to 0,
                    "راهنمایی / متوسطه (1)" to 1,
                    "دیپلم (2)" to 2,
                    "لیسانس (3)" to 3,
                    "فوق لیسانس و بالاتر (4)" to 4
                )
                educations.forEach { (label, value) ->
                    Row(
                        Modifier
                            .fillMaxWidth()
                            .selectable(
                                selected = (regData.education == value),
                                onClick = { regData = regData.copy(education = value) },
                                role = Role.RadioButton
                            )
                            .padding(vertical = 2.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        RadioButton(selected = (regData.education == value), onClick = null)
                        Text(text = label, modifier = Modifier.padding(start = 4.dp), fontSize = 13.sp)
                    }
                }

                Spacer(Modifier.height(8.dp))
                Text("شغل (Job):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Row(Modifier.fillMaxWidth()) {
                    listOf("خانه‌دار (0)" to 0, "بازنشسته (1)" to 1, "شاغل (2)" to 2).forEach { (label, value) ->
                        Row(
                            Modifier
                                .selectable(
                                    selected = (regData.job == value),
                                    onClick = { regData = regData.copy(job = value) },
                                    role = Role.RadioButton
                                )
                                .padding(horizontal = 6.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            RadioButton(selected = (regData.job == value), onClick = null)
                            Text(text = label, modifier = Modifier.padding(start = 4.dp), fontSize = 13.sp)
                        }
                    }
                }

                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = regData.familySize,
                        onValueChange = { regData = regData.copy(familySize = it) },
                        label = { Text("تعداد اعضای خانواده (FamilySize)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                    OutlinedTextField(
                        value = regData.kids,
                        onValueChange = { regData = regData.copy(kids = it) },
                        label = { Text("تعداد فرزندان (Kids)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(Modifier.height(8.dp))
                Text("وضعیت مسکن (HouseOwnership):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Row(Modifier.fillMaxWidth()) {
                    listOf("اجاره‌ای / رهن (1)" to 1, "صاحب‌خانه (2)" to 2).forEach { (label, value) ->
                        Row(
                            Modifier
                                .selectable(
                                    selected = (regData.houseOwnership == value),
                                    onClick = { regData = regData.copy(houseOwnership = value) },
                                    role = Role.RadioButton
                                )
                                .padding(horizontal = 8.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            RadioButton(selected = (regData.houseOwnership == value), onClick = null)
                            Text(text = label, modifier = Modifier.padding(start = 4.dp))
                        }
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // 2. Anthropometrics
            SectionCard(
                title = "۲. شاخص‌های تن‌سنجی (قد، وزن، BMI)",
                isExpanded = isAnthroExpanded,
                onToggle = { isAnthroExpanded = !isAnthroExpanded }
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = regData.weightKg,
                        onValueChange = { regData = regData.copy(weightKg = it) },
                        label = { Text("وزن به کیلوگرم (WeightKg)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                    OutlinedTextField(
                        value = regData.heightCm,
                        onValueChange = { regData = regData.copy(heightCm = it) },
                        label = { Text("قد به سانتی‌متر (HeightCm)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        singleLine = true,
                        modifier = Modifier.weight(1f)
                    )
                }
                Spacer(Modifier.height(12.dp))

                val bmiVal = regData.bmi
                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("شاخص توده بدنی (BMI خودکار):", fontWeight = FontWeight.Bold)
                        Text(
                            text = if (bmiVal != null) String.format("%.2f", bmiVal) else "---",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }

            Spacer(Modifier.height(12.dp))

            // 3. Narcotics & Tobacco
            SectionCard(
                title = "۳. دخانیات و مواد مخدر",
                isExpanded = isSubstanceExpanded,
                onToggle = { isSubstanceExpanded = !isSubstanceExpanded }
            ) {
                OutlinedTextField(
                    value = regData.cigar,
                    onValueChange = { regData = regData.copy(cigar = it) },
                    label = { Text("سیگار (Cigar)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = regData.ghelian,
                    onValueChange = { regData = regData.copy(ghelian = it) },
                    label = { Text("قلیان (Ghelian)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = regData.otherNarcotics,
                    onValueChange = { regData = regData.copy(otherNarcotics = it) },
                    label = { Text("سایر مواد مخدر (Other Narcotics)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }

            Spacer(Modifier.height(12.dp))

            // 4. Medications & Supplements
            SectionCard(
                title = "۴. داروها و مکمل‌ها",
                isExpanded = isMedsExpanded,
                onToggle = { isMedsExpanded = !isMedsExpanded }
            ) {
                BinarySelectRow("آسپرین (Aspirin)", regData.aspirin) { regData = regData.copy(aspirin = it) }
                BinarySelectRow("لووتیروکسین (Levotyroxin)", regData.levotyroxin) { regData = regData.copy(levotyroxin = it) }
                BinarySelectRow("ویتامین دی (VitD)", regData.vitD) { regData = regData.copy(vitD = it) }
                BinarySelectRow("مولتی‌ویتامین (Multivitamin)", regData.multivitamin) { regData = regData.copy(multivitamin = it) }
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = regData.statin,
                    onValueChange = { regData = regData.copy(statin = it) },
                    label = { Text("استاتین (Statin)") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }

            Spacer(Modifier.height(12.dp))

            // 5. Medical History
            SectionCard(
                title = "۵. سوابق بیماری‌ها",
                isExpanded = isMedicalExpanded,
                onToggle = { isMedicalExpanded = !isMedicalExpanded }
            ) {
                Text("دیابت (Diabetes):", fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                Row(Modifier.fillMaxWidth()) {
                    listOf("خیر (0)" to 0, "نوع ۱ (1)" to 1, "نوع ۲ (2)" to 2).forEach { (label, value) ->
                        Row(
                            Modifier
                                .selectable(
                                    selected = (regData.diabetes == value),
                                    onClick = { regData = regData.copy(diabetes = value) },
                                    role = Role.RadioButton
                                )
                                .padding(horizontal = 6.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            RadioButton(selected = (regData.diabetes == value), onClick = null)
                            Text(text = label, modifier = Modifier.padding(start = 4.dp), fontSize = 13.sp)
                        }
                    }
                }
                Spacer(Modifier.height(4.dp))
                BinarySelectRow("بیماری قلبی عروقی (CVD)", regData.cvd) { regData = regData.copy(cvd = it) }
                BinarySelectRow("فشار خون بالا (BP)", regData.bp) { regData = regData.copy(bp = it) }
                BinarySelectRow("میگرن (Migrane)", regData.migrane) { regData = regData.copy(migrane = it) }
                BinarySelectRow("بیماری‌های گوارشی (GID)", regData.gid) { regData = regData.copy(gid = it) }
                BinarySelectRow("سرطان (Cancer)", regData.cancer) { regData = regData.copy(cancer = it) }
            }

            Spacer(Modifier.height(12.dp))

            // 6. IPAQ (Activity questions)
            SectionCard(
                title = "۶. پرسشنامه فعالیت بدنی (IPAQ)",
                isExpanded = isIpaqExpanded,
                onToggle = { isIpaqExpanded = !isIpaqExpanded }
            ) {
                Text(
                    "پاسخ به فیلدهای فعالیت بدنی (IPAQ2 الی IPAQ25):",
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
                Spacer(Modifier.height(8.dp))

                val ipaqPairs = listOf(
                    (2 to 3) to "فعالیت‌های کاری شدید (ضریب ۸)",
                    (4 to 5) to "فعالیت‌های کاری متوسط (ضریب ۴)",
                    (6 to 7) to "پیاده‌روی کاری (ضریب ۳.۳)",
                    (8 to 9) to "نشستن در محیط کار (ضریب ۰)",
                    (10 to 11) to "حمل و نقل با دوچرخه (ضریب ۴)",
                    (12 to 13) to "پیاده‌روی برای جابجایی (ضریب ۳.۳)",
                    (14 to 15) to "کارهای سنگین منزل / حیاط (ضریب ۸)",
                    (16 to 17) to "کارهای متوسط منزل (ضریب ۴)",
                    (18 to 19) to "کارهای سبک منزل (ضریب ۳.۳)",
                    (20 to 21) to "پیاده‌روی تفریحی (ضریب ۳.۳)",
                    (22 to 23) to "ورزش شدید در اوقات فراغت (ضریب ۸)",
                    (24 to 25) to "ورزش متوسط در اوقات فراغت (ضریب ۴)"
                )

                ipaqPairs.forEach { (pair, desc) ->
                    val (col1, col2) = pair
                    Text(desc, fontWeight = FontWeight.SemiBold, fontSize = 13.sp)
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.padding(bottom = 8.dp)
                    ) {
                        OutlinedTextField(
                            value = regData.ipaq[col1] ?: "",
                            onValueChange = { newVal ->
                                val m = regData.ipaq.toMutableMap()
                                m[col1] = newVal
                                regData = regData.copy(ipaq = m)
                            },
                            label = { Text("IPAQ$col1 (تعداد روز)") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                        OutlinedTextField(
                            value = regData.ipaq[col2] ?: "",
                            onValueChange = { newVal ->
                                val m = regData.ipaq.toMutableMap()
                                m[col2] = newVal
                                regData = regData.copy(ipaq = m)
                            },
                            label = { Text("IPAQ$col2 (دقیقه در روز)") },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                            singleLine = true,
                            modifier = Modifier.weight(1f)
                        )
                    }
                }

                Surface(
                    shape = RoundedCornerShape(8.dp),
                    color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.5f),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("مجموع نمره MET فعالیت (IPAQMET):", fontWeight = FontWeight.Bold)
                        Text(
                            text = String.format("%.1f", regData.ipaqMet),
                            fontSize = 18.sp,
                            fontWeight = FontWeight.ExtraBold,
                            color = MaterialTheme.colorScheme.secondary
                        )
                    }
                }
            }

            Spacer(Modifier.height(24.dp))

            Button(
                onClick = {
                    if (regData.id.isBlank()) {
                        Toast.makeText(context, strings.fillAllFields, Toast.LENGTH_SHORT).show()
                    } else {
                        onProceedToFFQ(regData)
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(12.dp)
            ) {
                Text("تایید اطلاعات و ورود به پرسشنامه خوراک (FFQ)", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Spacer(Modifier.width(8.dp))
                Icon(Icons.Default.ArrowForward, contentDescription = null)
            }

            Spacer(Modifier.height(32.dp))
        }
    }
}

@Composable
fun SectionCard(
    title: String,
    isExpanded: Boolean,
    onToggle: () -> Unit,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f))
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onToggle() },
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.weight(1f)
                )
                Icon(
                    imageVector = if (isExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.primary
                )
            }
            AnimatedVisibility(visible = isExpanded) {
                Column(modifier = Modifier.padding(top = 14.dp)) {
                    content()
                }
            }
        }
    }
}

@Composable
fun BinarySelectRow(title: String, value: Int?, onSelect: (Int) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(title, fontSize = 14.sp, modifier = Modifier.weight(1f))
        Row {
            listOf("خیر (0)" to 0, "بله (1)" to 1).forEach { (label, optVal) ->
                Row(
                    Modifier
                        .selectable(
                            selected = (value == optVal),
                            onClick = { onSelect(optVal) },
                            role = Role.RadioButton
                        )
                        .padding(horizontal = 6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RadioButton(selected = (value == optVal), onClick = null)
                    Text(text = label, modifier = Modifier.padding(start = 2.dp), fontSize = 13.sp)
                }
            }
        }
    }
}
