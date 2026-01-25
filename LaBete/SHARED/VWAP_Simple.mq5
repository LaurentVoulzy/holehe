//+------------------------------------------------------------------+
//|                                              VWAP_Simple.mq5     |
//|                                    Copyright 2025, Yann - La Bête |
//|                                                                    |
//| VWAP SIMPLIFIÉ - TEST AFFICHAGE                                   |
//| Calcul sans reset journalier pour debug                          |
//+------------------------------------------------------------------+

#property copyright "Yann - La Bête"
#property link      ""
#property version   "1.00"
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
//| Initialization                                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, UpperBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(2, LowerBand1Buffer, INDICATOR_DATA);
    SetIndexBuffer(3, UpperBand2Buffer, INDICATOR_DATA);
    SetIndexBuffer(4, LowerBand2Buffer, INDICATOR_DATA);

    IndicatorSetString(INDICATOR_SHORTNAME, "VWAP Simple");
    IndicatorSetInteger(INDICATOR_DIGITS, _Digits);

    Print("✅ VWAP SIMPLE initialisé - TEST AFFICHAGE");
    return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Calculation                                                      |
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

    // Calculer sur les 100 dernières barres seulement
    int limit = MathMin(100, rates_total - prev_calculated);
    if(prev_calculated == 0)
        limit = MathMin(100, rates_total);

    for(int bar = limit - 1; bar >= 0; bar--)
    {
        double sumTPV = 0;
        double sumVol = 0;
        double sumSquares = 0;

        // Calculer VWAP sur les 50 dernières barres
        int lookback = MathMin(50, rates_total - bar);

        for(int i = 0; i < lookback; i++)
        {
            int idx = bar + i;
            if(idx >= rates_total)
                break;

            double tp = (high[idx] + low[idx] + close[idx]) / 3.0;
            double vol = (volume[idx] > 0) ? (double)volume[idx] : (double)tick_volume[idx];

            if(vol <= 0)
                vol = 1;

            sumTPV += tp * vol;
            sumVol += vol;
        }

        // VWAP
        double vwap = (sumVol > 0) ? sumTPV / sumVol : close[bar];
        VWAPBuffer[bar] = vwap;

        // Calculer écart-type
        sumSquares = 0;
        for(int i = 0; i < lookback; i++)
        {
            int idx = bar + i;
            if(idx >= rates_total)
                break;

            double tp = (high[idx] + low[idx] + close[idx]) / 3.0;
            double vol = (volume[idx] > 0) ? (double)volume[idx] : (double)tick_volume[idx];

            if(vol <= 0)
                vol = 1;

            double diff = tp - vwap;
            sumSquares += diff * diff * vol;
        }

        double variance = (sumVol > 0) ? sumSquares / sumVol : 0;
        double stdDev = MathSqrt(variance);

        // Bandes
        UpperBand1Buffer[bar] = vwap + stdDev;
        LowerBand1Buffer[bar] = vwap - stdDev;
        UpperBand2Buffer[bar] = vwap + (2 * stdDev);
        LowerBand2Buffer[bar] = vwap - (2 * stdDev);
    }

    return(rates_total);
}
