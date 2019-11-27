# Created by Fufu at 2019/10/9
@asn
Feature: AS 号管理
  请先清除数据(暂未开放删除操作)
  delete from bgp_asn where asn in (1, 99999990);

  @success
  Scenario Outline: 1. 添加 ASN (正例)
    Given 输入AS号和描述 "<asn>", "<asn_desc>"
    When 执行添加AS号
    Then AS号添加成功

    Examples:
      | asn      | asn_desc |
      | 1        | test_1   |
      | 99999990 | test_??? |

  @error
  Scenario Outline: 2. 添加 ASN (反例)
    Given 输入AS号和描述 "<asn>", "<asn_desc>"
    When 执行添加AS号
    Then AS号添加失败

    Examples:
      | asn  | asn_desc |
      | 0    | test_1   |
      | a123 | 123      |
      | -1   | test     |

  @error
  Scenario Outline: 3. 添加 ASN (反例)
    Given 仅输入AS号 "<asn>"
    When 执行添加AS号
    Then AS号添加失败

    Examples:
      | asn      |
      | 0        |
      | 123      |
      | -1       |
      | 99999990 |
