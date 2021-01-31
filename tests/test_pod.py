from solid_server import pod


def test_new_container_type():

    res = pod.new_container('test',
                            root=False,
                            format='ttl')

    assert type(res) is bytes


def test_new_acl_type():

    res = pod.new_acl(uri='test',
                      agent='agent',
                      scopes=['read', 'write', 'control'],
                      default=True,
                      format='ttl')

    assert type(res) is bytes


def test_append_acl_type():

    original_acl = pod.new_acl(uri='test',
                               agent='agent',
                               scopes=['read', 'write', 'control'],
                               default=True,
                               format='ttl')

    res = pod.append_acl(original_acl, 'test2', 'agent2')

    assert type(res) is bytes


def test_append_acl_numbers():

    original_acl = pod.new_acl(uri='test',
                               agent='agent',
                               scopes=['read', 'write', 'control'],
                               default=True,
                               format='ttl')

    res = pod.append_acl(original_acl, 'test2', 'agent2')

    assert '#authorization1' in res.decode('utf-8')
    assert '#authorization2' in res.decode('utf-8')
