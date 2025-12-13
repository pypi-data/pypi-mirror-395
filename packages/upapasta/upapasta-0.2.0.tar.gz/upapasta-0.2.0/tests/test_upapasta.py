# Tests for upapasta
from upapasta import main
import sys
import os


def test_parse_args_obfuscate_and_password(tmp_path, monkeypatch):
	# Simulate command line args parsing by temporarily overriding sys.argv
	argv = ["prog", str(tmp_path), "--obfuscate", "--rar-password", "secret123", "--nzb-password", "nzb123"]
	monkeypatch.setattr(sys, "argv", argv)
	args = main.parse_args()
	assert args.obfuscate is True
	assert args.rar_password == "secret123"
	assert args.nzb_password == "nzb123"


def test_parse_args_x_flag(monkeypatch, tmp_path):
	import sys
	argv = ["prog", str(tmp_path), "-x"]
	monkeypatch.setattr(sys, "argv", argv)
	args = main.parse_args()
	assert getattr(args, 'x', False) is True
	# Using -x must also set obfuscate attribute on args (main() behavior copies this)
	# parse_args doesn't change obfuscate, but orchestrator will; here we assert parse_args returns x flag


def test_dry_run_obfuscate_generates_random_rar(tmp_path):
	# Create a dummy folder to be passed as argument
	folder = tmp_path / "myfolder"
	folder.mkdir()

	orch = main.UpaPastaOrchestrator(
		folder_path=str(folder),
		dry_run=True,
		obfuscate=True,
	)
	assert orch.run_makerar() is True
	assert orch.rar_file is not None
	assert orch.rar_file.endswith('.rar')
	# Ensure the random name is different than the folder name
	assert os.path.basename(orch.rar_file) != f"{folder.name}.rar"


def test_orchestrator_run_dry_run_no_upload(tmp_path):
	# Create a dummy folder
	folder = tmp_path / "myrun"
	folder.mkdir()
	orch = main.UpaPastaOrchestrator(
		folder_path=str(folder),
		dry_run=True,
		skip_upload=True,
		obfuscate=True,
		rar_password="secret123",
		nzb_password="nzbpass",
	)
	rc = orch.run()
	assert rc == 0
	# After run, rar_file should be set (dry-run simulated)
	assert orch.rar_file is not None
	assert orch.rar_file.endswith('.rar')


def test_upload_dryrun_includes_nzb_password(tmp_path, capsys):
	from upapasta.upfolder import upload_to_usenet
	d = tmp_path / "job"
	d.mkdir()
	rar = d / "mypost.rar"
	par2 = d / "mypost.par2"
	rar.write_text("x")
	par2.write_text("x")

	rc = upload_to_usenet(str(rar), env_vars={'NNTP_HOST':'host','NNTP_USER':'u','NNTP_PASS':'p','USENET_GROUP':'alt.test','NNTP_PORT':'119'}, dry_run=True, subject='MySubject', group='alt.test', nzb_password='mypass')

	captured = capsys.readouterr()
	assert rc == 0
	assert 'MySubject (pwd: mypass)' in captured.out


def test_x_flag_generates_random_password_and_obfuscates(tmp_path):
	folder = tmp_path / "xfolder"
	folder.mkdir()
	orch = main.UpaPastaOrchestrator(folder_path=str(folder), dry_run=True, obfuscate=True)
	# Since obfuscate True, orchestrator should have generated a password
	assert orch.rar_password is not None
	assert orch.nzb_password is not None
	assert orch.rar_password == orch.nzb_password
	assert len(orch.rar_password) == 12
	# Running makerar in dry-run mode should generate an obfuscated rar filename
	assert orch.run_makerar() is True
	assert orch.rar_file is not None
	assert os.path.basename(orch.rar_file) != f"{folder.name}.rar"


def test_x_flag_overrides_user_password(tmp_path):
	# Ensure that when obfuscation (--x) is set, any user-provided password gets overridden
	folder = tmp_path / "xo"
	folder.mkdir()
	orch = main.UpaPastaOrchestrator(folder_path=str(folder), dry_run=True, obfuscate=True, rar_password='userpwd', nzb_password='usernzb')
	# Orchestrator should override provided passwords when obfuscate=True
	assert orch.rar_password != 'userpwd'
	assert orch.nzb_password != 'usernzb'
	assert orch.rar_password == orch.nzb_password
