//+------------------------------------------------------------------+
//|                                                  VWAP_V12.mq5     |
//|                                    Copyright 2025, Yann - La Bête |
//|                                                                    |
//| VWAP V12 (Volume Weighted Average Price) avec Bandes SD          |
//| - VWAP Daily (reset chaque jour à 00:00)                         |
//| - Bandes ±1σ, ±2σ (Support/Résistance basés sur volume)         |
//| - FIX V12.1: Calcul cumulatif corrigé                           |
//| - Utilisé par La Bête V12 pour détecter zones institutionnelles  |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property link      ""
#property version   "12.10"
#property indicator_chart_window
#property indicator_buffers 5
#property indicator_plots   5

// VWAP centrale
#property indicator_label1  "VWAP"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrDodgerBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2

// Bande +1σ (Résistance)
#property indicator_label2  "VWAP +1σ"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrOrangeRed
#property indicator_style2  STYLE_DOT
#property indicator_width2  1

// Bande -1σ (Support)
#property indicator_label3  "VWAP -1σ"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrLimeGreen
#property indicator_style3  STYLE_DOT
#property indicator_width3  1

// Bande +2σ (Résistance extrême)
#property indicator_label4  "VWAP +2σ"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrRed
#property indicator_style4  STYLE_DASH
#property indicator_width4  1

// Bande -2σ (Support extrême)
#property indicator_label5  "VWAP -2σ"
#property indicator_type5   DRAW_LINE
#property indicator_color5  clrGreen
#property indicator_style5  STYLE_DASH
#property indicator_width5  1

//--- Buffers indicateur
double VWAPBuffer[];
double UpperBand1Buffer[];
double LowerBand1Buffer[];
double UpperBand2Buffer[];
double LowerBand2Buffer[];

//--- Variables globales
datetime lastResetTime = 0;
double cumulativeTPV = 0;    // Cumulative (Typical Price × Volume)
double cumulativeVolume = 0; // Cumulative Volume
double cumulativeTPV2 = 0;   // Pour variance

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
    //--- Mapper les buffers
    SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, UpperBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(2, LowerBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(3, UpperBand2Buffer, INDICATOR_DATA);
    SetIndexBuffer(4, LowerBand2Buffer, INDICATOR_DATA);

    //--- Définir le début du dessin
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1);
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 1);
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 1);
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 1);
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 1);

    //--- Nom court
    IndicatorSetString(INDICATOR_SHORTNAME, "VWAP V12.1");

    //--- Précision
    IndicatorSetInteger(INDICATOR_DIGITS, _Digits);

    Print("✅ VWAP V12.1 initialisé - Bandes ±1σ, ±2σ (FIX calcul cumulatif)");
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
    //--- Vérifier données suffisantes
    if(rates_total < 2)
        return 0;

    //--- Définir array as series
    ArraySetAsSeries(time, true);
    ArraySetAsSeries(high, true);
    ArraySetAsSeries(low, true);
    ArraySetAsSeries(close, true);
    ArraySetAsSeries(tick_volume, true);
    ArraySetAsSeries(volume, true);

    //--- Variables
    int limit;
    datetime currentDayStart = 0;

    // Déterminer le début de la journée actuelle (00:00)
    MqlDateTime dt;
    TimeToStruct(time[0], dt);
    dt.hour = 0;
    dt.min = 0;
    dt.sec = 0;
    currentDayStart = StructToTime(dt);

    //--- Déterminer à partir de quelle barre calculer
    if(prev_calculated == 0 || lastResetTime != currentDayStart)
    {
        // Premier calcul ou nouvelle journée
        limit = rates_total - 1;

        // Trouver l'index du début de la journée
        for(int i = 0; i < rates_total; i++)
        {
            if(time[i] >= currentDayStart)
            {
                limit = i;
            }
            else
            {
                break;
            }
        }

        // Reset cumulative values
        cumulativeTPV = 0;
        cumulativeVolume = 0;
        cumulativeTPV2 = 0;
        lastResetTime = currentDayStart;
    }
    else
    {
        limit = rates_total - prev_calculated;
    }

    //--- Calcul VWAP et bandes (parcourir de l'ancien vers le récent)
    double tempTPV = 0;
    double tempVolume = 0;
    double tempTPV2 = 0;

    for(int i = limit; i >= 0; i--)
    {
        // Typical Price = (High + Low + Close) / 3
        double typicalPrice = (high[i] + low[i] + close[i]) / 3.0;

        // Volume (utiliser tick_volume si volume réel non disponible)
        double vol = (volume[i] > 0) ? (double)volume[i] : (double)tick_volume[i];

        if(vol <= 0)
            vol = 1; // Éviter division par zéro

        // Vérifier si même journée que currentDayStart
        MqlDateTime barDt;
        TimeToStruct(time[i], barDt);
        barDt.hour = 0;
        barDt.min = 0;
        barDt.sec = 0;
        datetime barDayStart = StructToTime(barDt);

        // Si nouvelle journée (changement), reset les cumuls temporaires
        if(i == limit || barDayStart != lastResetTime)
        {
            tempTPV = 0;
            tempVolume = 0;
            tempTPV2 = 0;
            lastResetTime = barDayStart;
        }

        // Accumuler
        tempTPV += (typicalPrice * vol);
        tempVolume += vol;

        // Calculer VWAP
        if(tempVolume > 0)
        {
            VWAPBuffer[i] = tempTPV / tempVolume;
        }
        else
        {
            VWAPBuffer[i] = typicalPrice;
        }

        // Calculer variance pour Standard Deviation
        double deviation = typicalPrice - VWAPBuffer[i];
        tempTPV2 += (deviation * deviation * vol);

        // Standard Deviation
        double variance = (tempVolume > 0) ? (tempTPV2 / tempVolume) : 0;
        double stdDev = MathSqrt(variance);

        // Bandes
        UpperBand1Buffer[i] = VWAPBuffer[i] + stdDev;       // +1σ
        LowerBand1Buffer[i] = VWAPBuffer[i] - stdDev;       // -1σ
        UpperBand2Buffer[i] = VWAPBuffer[i] + (2 * stdDev); // +2σ
        LowerBand2Buffer[i] = VWAPBuffer[i] - (2 * stdDev); // -2σ
    }

    // Sauvegarder les cumuls pour la barre actuelle
    cumulativeTPV = tempTPV;
    cumulativeVolume = tempVolume;
    cumulativeTPV2 = tempTPV2;

    //--- Retourner valeur de prev_calculated pour le prochain appel
    return(rates_total);
}

//+------------------------------------------------------------------+
//| Fonction pour obtenir VWAP et bandes (appelée par EA)           |
//+------------------------------------------------------------------+

// Cette fonction peut être appelée depuis un EA pour obtenir les valeurs
bool GetVWAPValues(double &vwap, double &upper1, double &lower1, double &upper2, double &lower2, int shift = 0)
{
    if(ArraySize(VWAPBuffer) <= shift)
        return false;

    vwap = VWAPBuffer[shift];
    upper1 = UpperBand1Buffer[shift];
    lower1 = LowerBand1Buffer[shift];
    upper2 = UpperBand2Buffer[shift];
    lower2 = LowerBand2Buffer[shift];

    return true;
}
