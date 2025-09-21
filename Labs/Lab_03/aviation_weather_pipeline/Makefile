.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "Starting data fetch process..."
	./fetch_metars.sh
	@echo "Data fetch completed. Raw data saved to raw_metars/ directory."

analyze: fetch
	@echo "Starting data analysis process..."
	./analyze_data.sh
	@echo "Data analysis completed. Results saved to weather_report.csv."
	@echo "Pipeline completed successfully!"

clean:
	@echo "Cleaning up workspace..."
	rm -rf raw_metars/
	rm -f weather_report.csv
	@echo "Cleanup completed."
