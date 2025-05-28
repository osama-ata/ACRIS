"""
Main entry point for the ACRIS system.
"""
import logging

# ...main logic will be implemented here...


def main() -> None:
	# Configure basic logging
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
		handlers=[
			logging.StreamHandler() # Log to console
		]
	)
	logging.info('ACRIS system initialized and logging configured.')
	print('ACRIS system entry point.')


if __name__ == '__main__':
	main()
