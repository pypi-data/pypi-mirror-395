from gradientcast import GradientCastFM

# Your production FM API key
FM_API_KEY = "7AoFAr3yaLUg7g8TZ30bAboU4G2zRrYBLZskk4dFN66e5ht5siQTJQQJ99BKAAAAAAAAAAAAINFRAZML1DrB"

def test_fm_single_series():
    """Test forecasting a single time series."""
    print("Testing GradientCastFM (production)...")
    
    fm = GradientCastFM(
        api_key=FM_API_KEY,
        environment="production"  # Uses prod URL
    )
    
    # Simple hourly data
    result = fm.forecast(
        input_data=[100, 120, 115, 130, 125, 140, 135, 150, 145, 160],
        horizon_len=5,
        freq="H"
    )
    
    print(f"Input: 10 hourly values")
    print(f"Forecast: {result.forecast['default']}")
    print(f"Processing time: {result.model_info.processing_time:.2f}s")
    print(f"Context length: {result.model_info.context_length}")
    print()
    return result

def test_fm_multi_series():
    """Test forecasting multiple series at once."""
    print("Testing multi-series forecast...")
    
    fm = GradientCastFM(api_key=FM_API_KEY)
    
    result = fm.forecast(
        input_data={
            "product_a": [100, 120, 115, 130, 125, 140, 135, 150],
            "product_b": [200, 220, 215, 230, 225, 240, 235, 250],
        },
        horizon_len=7,
        freq="D"
    )
    
    print(f"Product A forecast: {result['product_a']}")
    print(f"Product B forecast: {result['product_b']}")
    print()
    return result

def test_fm_to_dataframe():
    """Test pandas DataFrame conversion."""
    print("Testing DataFrame conversion...")
    
    fm = GradientCastFM(api_key=FM_API_KEY)
    
    result = fm.forecast(
        input_data={"sales": [100, 120, 115, 130, 125]},
        horizon_len=3,
        freq="D"
    )
    
    df = result.to_dataframe()
    print(df)
    print()
    return df

if __name__ == "__main__":
    test_fm_single_series()
    test_fm_multi_series()
    test_fm_to_dataframe()
    print("All FM tests passed!")