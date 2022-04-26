
const tosca = require('tosca.lib.utils');

exports.validate = function(v, rules) {
	if (arguments.length !== 2)
		throw 'must have 1 arguments';
	if ((rules.step === undefined) || (rules.offset === undefined))
		throw 'must provide "step" and "offset"';
	v = tosca.getComparable(v);
	let step = tosca.getComparable(rules.step);
	let offset = tosca.getComparable(rules.offset);
	return value % self.step == self.offset;
};
