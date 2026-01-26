//+------------------------------------------------------------------+
//|                                                  VWAP_V12.mq5     |
//|                                    Copyright 2025, Yann - La Bête |
//|                                                                    |
//| VWAP V13 - SIMPLIFIÉ (comme VWAP market qui fonctionne)          |
//| - Reset daily                                                     |
//| - Bandes ±1σ, ±2σ                                                |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property link      ""
#property version   "13.00"
#property indicator_chart_window
#property indicator_buffers 5
#property indicator_plots   5

// VWAP centrale
#property indicator_label1  "VWAP"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrDodgerBlue
#property indicator_style1  STYLE_SOLID
#property indicator_width1  3

// Bande +1σ
#property indicator_label2  "VWAP +1σ"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrRed
#property indicator_style2  STYLE_SOLID
#property indicator_width2  2

// Bande -1σ
#property indicator_label3  "VWAP -1σ"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrLime
#property indicator_style3  STYLE_SOLID
#property indicator_width3  2

// Bande +2σ
#property indicator_label4  "VWAP +2σ"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrOrangeRed
#property indicator_style4  STYLE_DOT
#property indicator_width4  1

// Bande -2σ
#property indicator_label5  "VWAP -2σ"
#property indicator_type5   DRAW_LINE
#property indicator_color5  clrGreenYellow
#property indicator_style5  STYLE_DOT
#property indicator_width5  1

//--- Buffers
double VWAPBuffer[];
double UpperBand1Buffer[];
double LowerBand1Buffer[];
double UpperBand2Buffer[];
double LowerBand2Buffer[];

//+------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, UpperBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(2, LowerBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(3, UpperBand2Buffer, INDICATOR_DATA);
    SetIndexBuffer(4, LowerBand2Buffer, INDICATOR_DATA);

    IndicatorSetString(INDICATOR_SHORTNAME, "VWAP V13");
    IndicatorSetInteger(INDICATOR_DIGITS, _Digits);

    Print("✅ VWAP V13 initialisé - Version simplifiée");
    return(INIT_SUCCEEDED);
}

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
    if(rates_total < 10)
        return 0;

    int start = 0;
    if(prev_calculated > 0)
        start = prev_calculated - 1;

    for(int i = start; i < rates_total; i++)
    {
        // Trouver le début de la journée
        MqlDateTime dt;
        TimeToStruct(time[i], dt);
        dt.hour = 0;
        dt.min = 0;
        dt.sec = 0;
        datetime dayStart = StructToTime(dt);

        // Trouver l'index du début de la journée
        int dayStartIndex = i;
        for(int j = i; j >= 0; j--)
        {
            if(time[j] < dayStart)
            {
                dayStartIndex = j + 1;
                break;
            }
            if(j == 0)
                dayStartIndex = 0;
        }

        // Calculer VWAP depuis le début de la journée
        double sumPV = 0;
        double sumV = 0;

        for(int j = dayStartIndex; j <= i; j++)
        {
            double typicalPrice = (high[j] + low[j] + close[j]) / 3.0;
            double vol = (volume[j] > 0) ? (double)volume[j] : (double)tick_volume[j];
            if(vol <= 0) vol = 1;

            sumPV += typicalPrice * vol;
            sumV += vol;
        }

        // VWAP
        VWAPBuffer[i] = (sumV > 0) ? sumPV / sumV : close[i];

        // Calculer écart-type
        double sumSquares = 0;
        for(int j = dayStartIndex; j <= i; j++)
        {
            double typicalPrice = (high[j] + low[j] + close[j]) / 3.0;
            double vol = (volume[j] > 0) ? (double)volume[j] : (double)tick_volume[j];
            if(vol <= 0) vol = 1;

            double diff = typicalPrice - VWAPBuffer[i];
            sumSquares += diff * diff * vol;
        }

        double variance = (sumV > 0) ? sumSquares / sumV : 0;
        double stdDev = MathSqrt(variance);

        // Bandes
        UpperBand1Buffer[i] = VWAPBuffer[i] + stdDev;
        LowerBand1Buffer[i] = VWAPBuffer[i] - stdDev;
        UpperBand2Buffer[i] = VWAPBuffer[i] + (2 * stdDev);
        LowerBand2Buffer[i] = VWAPBuffer[i] - (2 * stdDev);
    }

    return(rates_total);
}

//+------------------------------------------------------------------+
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
