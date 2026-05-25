test:
	python -m pytest -q

layout:
	find . -maxdepth 3 -type f | sort

generate-examples:
	python scripts/generate_modinv_certificate.py --bits 8 --modulus 251 --count 32 --out examples/inv_8bit.json
	python scripts/generate_modinv_certificate.py --bits 16 --modulus 65521 --count 64 --out examples/inv_16bit.json

verify-examples:
	python -m verifier.certificate examples/inv_8bit.json
	python -m verifier.certificate examples/inv_16bit.json

attach-circuit-example:
	python scripts/attach_circuit_to_certificate.py --cert examples/inv_8bit.json --circuit circuits/toy_modinv_stub_8bit.json --out examples/inv_8bit_with_circuit.json

verify-circuit-example:
	python -m verifier.certificate examples/inv_8bit_with_circuit.json --circuit circuits/toy_modinv_stub_8bit.json

verify-all:
	python -m verifier.certificate examples/inv_8bit.json
	python -m verifier.certificate examples/inv_16bit.json
	python -m verifier.certificate examples/inv_8bit_with_circuit.json --circuit circuits/toy_modinv_stub_8bit.json

report:
	python scripts/generate_certificate_report.py

generate-toy-circuits:
	python scripts/generate_toy_circuits.py

toy-circuit-report:
	python scripts/generate_toy_circuit_report.py

generate-toy-certificates:
	python scripts/generate_toy_circuit_certificates.py

verify-toy-certificates:
	python -m verifier.certificate examples/toy_cnot_copy_cert.json --circuit circuits/toy_cnot_copy.json
	python -m verifier.certificate examples/toy_toffoli_and_cert.json --circuit circuits/toy_toffoli_and.json
	python -m verifier.certificate examples/toy_swap_cert.json --circuit circuits/toy_swap.json

generate-add-mod-2n:
	python scripts/generate_add_mod_2n_circuit.py --n 2 --out circuits/toy_add_mod_2n_n2.json
	python scripts/generate_add_mod_2n_certificate.py --circuit circuits/toy_add_mod_2n_n2.json --out examples/toy_add_mod_2n_n2_cert.json

verify-add-mod-2n:
	python -m verifier.certificate examples/toy_add_mod_2n_n2_cert.json --circuit circuits/toy_add_mod_2n_n2.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find paper -type f \( -name "*.aux" -o -name "*.bbl" -o -name "*.blg" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*.synctex.gz" \) -delete