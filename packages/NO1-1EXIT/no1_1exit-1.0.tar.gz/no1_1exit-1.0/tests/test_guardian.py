import guardian

def test_enable():
    guardian.enable()
    assert guardian._LOCK == True

def test_disable():
    guardian.disable()
    assert guardian._LOCK == False

# يمكنك إضافة اختبارات أخرى لتغطية الحالات المختلفة
