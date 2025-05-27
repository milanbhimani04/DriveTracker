function validateTableDetais() {

	if ($('#tableType').val().trim() === '') {
		$('#tableType').focus()
		showErrorToast('Please select table type')
		return false;
	} else if ($('#numberOfTable').val().trim() === '') {
		$('#numberOfTable').focus()
		showErrorToast('Please enter number of table')		
		return false;
	}else {
		return true;
	}
}