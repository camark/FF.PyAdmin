# Created by Fufu at 2019/10/9
@bgp
Feature: BGP管理
  请先清除数据(暂未开放删除操作)
  delete from bgp_bgp where bgp_asn in (1, 99999990);

  @success
  Scenario Outline: 1. 添加 BGP (正例)
    Given 输入BGP-IP, ASN和描述 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>"
    When 执行添加BGP操作
    Then BGP-IP添加成功

    Examples:
      | bgp_ip      | bgp_asn  | bgp_desc     |
      | 127.0.0.127 | 1        | test_bgp     |
      | 8.8.8.0     | 99999990 | test_bgp_??? |

  @error
  Scenario Outline: 2. 添加 BGP (反例)
    Given 输入BGP-IP和描述, ASN错误 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>"
    When 执行添加BGP操作
    Then BGP添加失败

    Examples:
      | bgp_ip   | bgp_asn  | bgp_desc |
      | 1.1.1.1  | 99999998 | test_1   |
      | 1.1.1.1  | 0        | test_1   |
      | 10.0.0.1 | a123     | 123      |
      | 0.0.0.1  | -1       | test     |

  @error
  Scenario Outline: 3. 添加 BGP (反例)
    Given BGP-IP输入错误 "<bgp_ip>", "<bgp_asn>", "<bgp_desc>"
    When 执行添加BGP操作
    Then BGP添加失败

    Examples:
      | bgp_ip       | bgp_asn  | bgp_desc     |
      | abc          | 1        | test_bgp     |
      | -1           | 1        | test_bgp     |
      | 127.0.0.256  | 1        | test_bgp     |
      | 127.0.0.1127 | 1        | test_bgp     |
      | 8.8.8.       | 99999990 | test_bgp_??? |
      | 123          | 1        | test_bgp     |
