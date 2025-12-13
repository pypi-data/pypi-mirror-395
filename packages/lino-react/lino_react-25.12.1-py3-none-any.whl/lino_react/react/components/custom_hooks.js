Storage.prototype.setObject = function (key, value, stringify = JSON.stringify) {
    this.setItem(key, stringify(value));
};

Storage.prototype.getObject = function (key, parse = JSON.parse) {
    var value = this.getItem(key);
    return value && parse(value);
};

Storage.prototype.updateObject = function (key, values) {
    this.setObject(key, Object.assign(this.getObject(key), values))
}

Storage.prototype.safeClear = function () {
    let keepable = this.getItem('clearsafe');
    this.clear();
    this.setItem('clearsafe', keepable);
};
