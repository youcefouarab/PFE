
// [TOSCA-Simple-Profile-YAML-v1.3] @ 3.6.3
// [TOSCA-Simple-Profile-YAML-v1.2] @ 3.6.3
// [TOSCA-Simple-Profile-YAML-v1.1] @ 3.5.2
// [TOSCA-Simple-Profile-YAML-v1.0] @ 3.5.2

const tosca = require('tosca.lib.utils');

exports.validate = function(v) {
	let values = Array.prototype.slice.call(arguments, 1);
	for (let i = 0, l = values.length; i < l; i++)
		if (tosca.deepEqual(values[i], v))
			return true;
	return false;
};
