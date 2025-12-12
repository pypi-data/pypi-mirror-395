import textwrap

from sila.framework.fdl.serializer import Serializer


class TestResult:
    def test_should_have_default_result(self):
        # Create serializer
        serializer = Serializer()

        # Assert that the method returns the correct value
        assert serializer.result() == ""

    def test_should_set_result(self):
        # Create serializer
        serializer = Serializer()

        # Set result
        serializer.write("Hello, World!")

        # Assert that the method returns the correct value
        assert serializer.result() == "Hello, World!\n"


class TestStartElement:
    def test_should_write_start_element(self):
        # Create serializer
        serializer = Serializer()

        # Start element
        serializer.start_element("Root")

        # Assert that the method returns the correct value
        assert serializer.result() == "<Root>\n"


class TestEndElement:
    def test_should_write_end_element(self):
        # Create serializer
        serializer = Serializer()

        # End element
        serializer.end_element("Root")

        # Assert that the method returns the correct value
        assert serializer.result() == "</Root>\n"


class TestWriteString:
    def test_should_write_string(self):
        # Create serializer
        serializer = Serializer()

        # Write string
        serializer.write_str("Element", "Hello, World!")

        # Assert that the method returns the correct value
        assert serializer.result() == textwrap.dedent(
            """\
            <Element>Hello, World!</Element>
            """
        )

    def test_should_write_string_in_element(self):
        # Create serializer
        serializer = Serializer()

        # Write string
        serializer.start_element("Root")
        serializer.write_str("Element", "Hello, World!")
        serializer.end_element("Root")

        # Assert that the method returns the correct value
        assert serializer.result() == textwrap.dedent(
            """\
            <Root>
              <Element>Hello, World!</Element>
            </Root>
            """
        )

    def test_should_write_long_string(self):
        # Create serializer
        serializer = Serializer()

        # Write string
        serializer.start_element("Root")
        serializer.write_str(
            "Element",
            (
                "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor "
                "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et "
                "accusam et justo duo dolores et ea rebum."
            ),
        )
        serializer.end_element("Root")

        # Assert that the method returns the correct value
        assert serializer.result() == textwrap.dedent(
            """\
            <Root>
              <Element>
                Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
                invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
                accusam et justo duo dolores et ea rebum.
              </Element>
            </Root>
            """
        )


class TestSerialize:
    def test_should_handle_noop(self):
        # Create handler
        def handler(serializer: Serializer):
            pass

        # Write datetime
        xml = Serializer.serialize(handler)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            """
        )

    def test_should_handle_elements(self):
        # Create handler
        def handler(serializer: Serializer):
            serializer.start_element("Root")
            serializer.write_str("Element", "Hello, World!")
            serializer.end_element("Root")

        # Write datetime
        xml = Serializer.serialize(handler)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Root>
              <Element>Hello, World!</Element>
            </Root>
            """
        )

    def test_should_handle_nested_elements(self):
        # Create handler
        def element_handler(serializer: Serializer):
            serializer.write_str("Element", "Hello, World!")

        def root_handler(serializer: Serializer):
            serializer.start_element("Root")
            element_handler(serializer)
            serializer.end_element("Root")

        # Write datetime
        xml = Serializer.serialize(root_handler)

        # Assert that the method returns the correct value
        assert xml == textwrap.dedent(
            """\
            <Root>
              <Element>Hello, World!</Element>
            </Root>
            """
        )
